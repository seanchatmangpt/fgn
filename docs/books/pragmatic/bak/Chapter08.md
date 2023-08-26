```python
# Import necessary libraries
from typing import Union, Dict
import os
import time
import json
import openai

# Define hyper-advanced constants for error handling
DEFAULT_PROMPT = "Translate this english text to python code: "
DEFAULT_SYS_MSG = "System failed to understand the message. Please try again."
DEFAULT_MODEL = "text-davinci-002"
DEFAULT_MAX_RETRY = 3
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_INITIAL_WAIT = 1

# A class representing your unique PragmaticProgrammerAGIAgent
class PragmaticProgrammerAGIAgent:
    def __init__(self, openai_api_key: str) -> None:
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        
        self.project_structure = {
            "src": ["__init__.py"],
            "tests": ["__init__.py"],
            ".github": {"workflows": ["test.yaml"]},
            "domain": ["__init__.py"],
            "infrastructure": ["docker-compose.yaml"],
            "requirements.txt": [],
        }

    def tracer_bullet(self, filepath: str, prompt: str, retry: int = DEFAULT_MAX_RETRY,
                      backoff_factor: int = DEFAULT_BACKOFF_FACTOR,
                      initial_wait: int = DEFAULT_INITIAL_WAIT ) -> None:
        """
        Method to create an end-to-end 'tracer bullet' file that 
        passes through the architecture layers.
        """
        if retry < 0:
            raise Exception("Maximum retries exceeded.")

        try:
            # Generate code using OpenAI's Codex
            codex_response = openai.Completion.create(
                engine=DEFAULT_MODEL,
                prompt=prompt,
                max_tokens=60,
                temperature=0.5
            )

            # Decompose the file path into directory and file
            paths = filepath.split('/')
            directory = '/'.join(paths[:-1])
            file = paths[-1]

            # Create directory if not exists
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write generated code into the file
            with open(filepath, "w") as f:
                f.write(codex_response.choices[0].text.strip())

        except Exception as e: 
            time.sleep(initial_wait * (backoff_factor ** (DEFAULT_MAX_RETRY - retry - 1)))
            self.tracer_bullet(filepath, prompt, retry-1)

    def generate_project(self, project_structure: Dict, parent_dir: str='') -> None:
        """
        Method to generate project structure with tracer bullets
        """
        prompt = f"Translate this english text to python code: create a blank python file"

        for key, value in project_structure.items():
            # Check if the key denotes a directory
            if isinstance(value, list):
                for file in value:
                    self.tracer_bullet(os.path.join(parent_dir, key, file), prompt)

            # Check if the key denotes a nested directory structure
            elif isinstance(value, dict):
                self.generate_project(value, os.path.join(parent_dir, key))

            # check if the key denotes a file
            else:
                self.tracer_bullet(os.path.join(parent_dir, key), prompt)

agent = PragmaticProgrammerAGIAgent("<YOUR_OPENAI_API_KEY>")
agent.generate_project(agent.project_structure)
```