"""Receipt-bound actuation for FGN.

Every externally consequential operation is admitted and journaled before it is
attempted. The initial receipt remains replayable even if consequence
observation or final receipt enrichment fails.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional


RECEIPT_SCHEMA = "https://chatman.ai/schemas/brce-receipt/v1"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Receipt:
    receipt_id: str
    intent_id: str
    action: str
    subject: str
    status: str
    phase: str
    started_at: str
    completed_at: Optional[str] = None
    authority: str = "local-user"
    input_sha256: Optional[str] = None
    output_sha256: Optional[str] = None
    consequence: dict[str, Any] = field(default_factory=dict)
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    schema: str = RECEIPT_SCHEMA

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActuationRefused(PermissionError):
    def __init__(self, message: str, receipt: Receipt):
        super().__init__(message)
        self.receipt = receipt


class Broker:
    """The exclusive FGN DO boundary.

    Receipt files are the broker trust root. An admitted receipt is durably
    written before target mutation, clipboard mutation, or subprocess launch.
    """

    def __init__(self, receipt_dir: str | os.PathLike[str] | None = None):
        configured = receipt_dir or os.getenv("FGN_RECEIPT_DIR")
        self.receipt_dir = Path(configured or Path.home() / ".fgn" / "receipts")
        self.receipt_dir.mkdir(parents=True, exist_ok=True)

    def _receipt_path(self, receipt: Receipt) -> Path:
        return self.receipt_dir / f"{receipt.receipt_id}.json"

    def _persist(self, receipt: Receipt) -> Path:
        path = self._receipt_path(receipt)
        payload = json.dumps(receipt.to_dict(), indent=2, sort_keys=True) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=self.receipt_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        return path

    def _begin(self, action: str, subject: str, input_bytes: bytes) -> Receipt:
        receipt = Receipt(
            receipt_id=str(uuid.uuid4()),
            intent_id=str(uuid.uuid4()),
            action=action,
            subject=subject,
            status="PARTIAL_ALIVE",
            phase="admitted",
            started_at=_utc_now(),
            input_sha256=_sha256(input_bytes),
        )
        self._persist(receipt)
        return receipt

    def _finish(
        self,
        receipt: Receipt,
        *,
        status: str,
        output_bytes: bytes | None = None,
        consequence: Mapping[str, Any] | None = None,
        error: BaseException | None = None,
    ) -> Receipt:
        receipt.status = status
        receipt.phase = "verified" if status == "ALIVE" else "observed-failure"
        receipt.completed_at = _utc_now()
        if output_bytes is not None:
            receipt.output_sha256 = _sha256(output_bytes)
        if consequence:
            receipt.consequence = dict(consequence)
        if error is not None:
            receipt.error_type = type(error).__name__
            receipt.error_message = str(error)
        self._persist(receipt)
        return receipt

    @staticmethod
    def _failure_status(error: BaseException) -> str:
        if isinstance(error, PermissionError):
            return "REFUSED:PERMISSION_DENIED"
        if isinstance(error, FileNotFoundError):
            return "BLOCKED"
        return "BUILD_BROKEN"

    def write_text(
        self,
        path: str | os.PathLike[str],
        content: str,
        *,
        append: bool = False,
        encoding: str = "utf-8",
    ) -> Receipt:
        target = Path(path).expanduser().absolute()
        requested = content.encode(encoding)
        receipt = self._begin("file.write", str(target), requested)
        temp_name: Optional[str] = None
        try:
            existing = target.read_text(encoding=encoding) if append and target.exists() else ""
            final_content = existing + content
            final_bytes = final_content.encode(encoding)
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
            with os.fdopen(fd, "w", encoding=encoding) as handle:
                handle.write(final_content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, target)
            temp_name = None
            observed = target.read_bytes()
            if observed != final_bytes:
                raise OSError("post-write observation did not match admitted bytes")
            return self._finish(
                receipt,
                status="ALIVE",
                output_bytes=observed,
                consequence={"bytes": len(observed), "append": append},
            )
        except BaseException as error:
            self._finish(receipt, status=self._failure_status(error), error=error)
            raise
        finally:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)

    def copy_text(self, content: str) -> Receipt:
        payload = content.encode("utf-8")
        receipt = self._begin("clipboard.copy", "system-clipboard", payload)
        try:
            import pyperclip

            pyperclip.copy(content)
            return self._finish(
                receipt,
                status="ALIVE",
                output_bytes=payload,
                consequence={"characters": len(content)},
            )
        except BaseException as error:
            return self._finish(
                receipt,
                status="UNSUPPORTED" if type(error).__name__ == "PyperclipException" else self._failure_status(error),
                error=error,
            )

    def run_shell(
        self,
        command: str,
        *,
        admitted: bool = False,
        cwd: str | os.PathLike[str] | None = None,
        timeout: float | None = None,
        env: Mapping[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], Receipt]:
        subject = str(Path(cwd).absolute()) if cwd else os.getcwd()
        receipt = self._begin("process.shell", subject, command.encode("utf-8"))
        if not admitted:
            message = "shell execution requires explicit admission"
            self._finish(
                receipt,
                status="REFUSED:SHELL_AUTHORITY_REQUIRED",
                error=PermissionError(message),
            )
            raise ActuationRefused(f"{message}; receipt={receipt.receipt_id}", receipt)
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                env=dict(env) if env is not None else None,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            combined = (result.stdout + result.stderr).encode("utf-8")
            status = "ALIVE" if result.returncode == 0 else "BUILD_BROKEN"
            self._finish(
                receipt,
                status=status,
                output_bytes=combined,
                consequence={
                    "exit_code": result.returncode,
                    "stdout_sha256": _sha256(result.stdout.encode("utf-8")),
                    "stderr_sha256": _sha256(result.stderr.encode("utf-8")),
                },
            )
            return result, receipt
        except BaseException as error:
            self._finish(receipt, status=self._failure_status(error), error=error)
            raise
