# fgn/utils/output_manager.py
from dataclasses import dataclass
from typing import Optional

import pyperclip
from rich import print
from rich.markdown import Markdown

from fgn.utils.file_operations import extract_markdown
from fgn.utils.llm_operations import generate_output_file


@dataclass
class OutputManager:
    output: Optional[str] = None
    no_copy: bool = False
    auto_output: bool = False
    verbose: bool = False
    extension: str = "md"

    def handle_output(
        self, response: str, extract_md: bool = False, append: Optional[str] = False
    ) -> None:
        if extract_md:
            response = extract_markdown(response)
            if self.verbose:
                print("Extracting markdown...")
                print(response)
        output = self.output
        no_copy = self.no_copy
        auto_output = self.auto_output

        if output:
            self.save_to_file(response, output, append=append)
        if auto_output:
            self.save_to_file(response, extension=self.extension)
        if not no_copy:
            pyperclip.copy(response)
            if self.verbose:
                print("The output has been saved to clipboard.")

        md = Markdown(str(response))
        print(md)

    def save_to_file(
        self,
        response: str,
        filename: Optional[str] = None,
        extension: str = "md",
        append: Optional[bool] = False,
    ) -> None:
        if not filename:
            filename = generate_output_file(response, extension=extension)
        if append:
            with open(filename, "a") as output_file:
                output_file.write("\n\n" + response)
        else:
            with open(filename, "w") as output_file:
                output_file.write(response)
        if self.verbose:
            print(f"The output has been saved to {filename}.")
