from __future__ import annotations

import asyncio
import json
import os
import shlex
import threading
from typing import Any, Dict, List, Mapping, Optional

from fgn.core.broker import Broker, Receipt

DEFAULT_MODEL = "llama-2-13b-chat.ggmlv3.q4_0.bin"
DEFAULT_LLAMA_HOME = os.getenv("LOCAL_LLAMA_HOME", str(os.path.expanduser("~/.local/share/llama.cpp")))
DEFAULT_MAX_TOKENS = 2048
DEFAULT_THREADS = 8
DEFAULT_NGL = 1
DEFAULT_C_FLAG = 2048
DEFAULT_TEMP = 0.7
DEFAULT_REPEAT_PENALTY = 1.1
DEFAULT_N_FLAG = -1

try:
    from langchain.callbacks.manager import CallbackManagerForLLMRun
    from langchain.llms.base import LLM
except ImportError:
    CallbackManagerForLLMRun = Any

    class LLM:  # type: ignore[no-redef]
        """Compatibility base when LangChain is not installed."""


class LocalLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "local_llama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> str:
        del run_manager
        return LocalLlamaClient().complete(prompt=prompt, stop=stop, **kwargs)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": DEFAULT_MODEL}


class LocalLlamaClient:
    """Execute an admitted local llama.cpp command through BRCE."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        llama_home: str = DEFAULT_LLAMA_HOME,
        *,
        broker: Broker | None = None,
    ):
        self.model = model
        self.llama_home = llama_home
        self.broker = broker or Broker()
        self.lock = threading.Lock()
        self.last_receipt: Receipt | None = None

    def _execute(self, command: list[str]) -> str:
        result, receipt = self.broker.run_shell(
            shlex.join(command),
            admitted=True,
            cwd=self.llama_home,
        )
        self.last_receipt = receipt
        if result.returncode != 0:
            raise RuntimeError(
                f"local Llama failed with exit {result.returncode}; receipt={receipt.receipt_id}"
            )
        return result.stdout.strip()

    async def acomplete(self, *args, **kwargs) -> str:
        command = self.get_command(*args, **kwargs)
        return await asyncio.to_thread(self._execute, command)

    async def achat(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, str]] | None = None,
        **kwargs,
    ) -> str:
        del functions
        prompt = "\n".join(message["content"] for message in messages)
        return await self.acomplete(prompt=prompt, **kwargs)

    def chat(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, str]] | None = None,
        *args,
        **kwargs,
    ) -> str:
        functions_text = "".join(json.dumps(function, indent=4) for function in (functions or []))
        system = messages[0].get("content", "") if messages else ""
        user = "\n".join(message["content"] for message in messages[1:])
        prompt = f"[INST]<<SYS>>{system}<</SYS>>{user}{functions_text}[/INST]"
        kwargs.setdefault("max_tokens", DEFAULT_MAX_TOKENS)
        return self.complete(prompt=prompt[:1000], *args, **kwargs)

    def complete(self, *args, **kwargs) -> str:
        command = self.get_command(*args, **kwargs)
        with self.lock:
            return self._execute(command)

    def get_model_info(self) -> dict[str, str]:
        return {"model": self.model, "description": "Local Llama model", "version": "2"}

    def _process_functions(self, functions: List[Dict[str, str]]):
        return functions

    def get_command(self, *args, **kwargs) -> list[str]:
        del args
        return [
            os.path.join(self.llama_home, "main"),
            "-t",
            str(kwargs.get("threads", DEFAULT_THREADS)),
            "-ngl",
            str(kwargs.get("ngl", DEFAULT_NGL)),
            "-m",
            os.path.join(self.llama_home, self.model),
            "-c",
            str(kwargs.get("c_flag", DEFAULT_C_FLAG)),
            "--temp",
            str(kwargs.get("temp", DEFAULT_TEMP)),
            "--repeat_penalty",
            str(kwargs.get("repeat_penalty", DEFAULT_REPEAT_PENALTY)),
            "-n",
            str(kwargs.get("n_flag", DEFAULT_N_FLAG)),
            "-p",
            str(kwargs.get("prompt", "")),
        ]
