from dataclasses import dataclass, field
from typing import Optional

from rich import print
from rich.markdown import Markdown

from fgn.core.broker import Broker, Receipt
from fgn.utils.file_operations import extract_markdown
from fgn.utils.llm_operations import generate_output_file


@dataclass
class OutputManager:
    output: Optional[str] = None
    no_copy: bool = False
    auto_output: bool = False
    verbose: bool = False
    extension: str = "md"
    broker: Broker = field(default_factory=Broker)

    def handle_output(self, response: str, extract_md: bool = False, append: bool = False) -> list[Receipt]:
        if extract_md:
            response = extract_markdown(response)
        receipts: list[Receipt] = []
        if self.output:
            receipts.append(self.save_to_file(response, self.output, append=append))
        if self.auto_output:
            receipts.append(self.save_to_file(response, extension=self.extension))
        if not self.no_copy:
            clipboard_receipt = self.broker.copy_text(response)
            receipts.append(clipboard_receipt)
            if self.verbose and clipboard_receipt.status != "ALIVE":
                print(f"Clipboard {clipboard_receipt.status}: {clipboard_receipt.error_message}")
        print(Markdown(str(response)))
        return receipts

    def save_to_file(self, response: str, filename: Optional[str] = None, extension: str = "md", append: bool = False) -> Receipt:
        target = filename or generate_output_file(response, extension=extension)
        receipt = self.broker.write_text(target, response if not append else "\n\n" + response, append=append)
        if self.verbose:
            print(f"Saved {target}; receipt={receipt.receipt_id}")
        return receipt
