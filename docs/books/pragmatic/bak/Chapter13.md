```python
import os
from openai import OpenAI, APIError
from typing import Any, List
import docker
import pytest
import git
import json

class PragmaticProgrammerAGIAgent:
    """
    The PragmaticProgrammerAGIAgent class builds advanced systems, implements the end-to-end tracer bullet 
    strategy and generates system files. It leverages DDD, docker compose, git actions, pytest, etc.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.docker_client = docker.from_env()
        self.git_repo = git.Repo()

    def openai_completion(self, prompt: str) -> str:
        try:
            response = self.client.Completion.create(
                engine="davinci-codex", 
                prompt=prompt, 
                temperature=0.5, 
                max_tokens=100
            )
            return response.choices[0].text.strip()
        except APIError as e:
            return str(e)

    def create_file_from_template(self, template: str, filename: str) -> str:
        content = self.openai_completion(prompt=template)
        with open(filename, 'w') as file:
            file.write(content)
        return filename

    def add_commit_push(self, filename: str, message: str) -> str:
        self.git_repo.index.add([filename])
        self.git_repo.index.commit(message)
        origin = self.git_repo.remote(name='origin')
        origin.pull()
        origin.push()
        return "Changes pushed to repository."

    def create_docker_compose_file(self) -> str:
        docker_compose_template = """
        version: '3'
        services:
            app:
                build: .
                ports:
                - "5000:5000"
        """
        docker_compose_filename = "docker-compose.yml"
        return self.create_file_from_template(docker_compose_template, docker_compose_filename)

    def create_pytest_file(self, funcs: List[str]) -> str:
        pytest_template = f"""
        import pytest
        {'\n'.join([f'def test_{func}():\n    assert {func}() == True' for func in funcs])}
        """
        pytest_filename = "test_funcs.py"
        return self.create_file_from_template(pytest_template, pytest_filename)

    def create_git_action_file(self) -> str:
        git_action_template = """
        name: Python package
        on: [push]
        jobs:
            build:
                runs-on: ubuntu-latest
                steps:
                - uses: actions/checkout@v2
                - name: Set up Python
                  uses: actions/setup-python@v2
                  with:
                      python-version: '3.x'
                - name: Install dependencies
                  run: |
                      python -m pip install --upgrade pip
                      pip install -r requirements.txt
                - name: Test with pytest
                  run: pytest
        """
        git_action_filename = ".github/workflows/python-package.yml"
        return self.create_file_from_template(git_action_template, git_action_filename)

    def tracer_bullet_implementation(self, route: str, method: str, response: str) -> str:
        """
        Create an end-to-end tracer bullet implementation, i.e., a minimal end-to-end implementation of a 
        system feature from the user interface to the data store.
        """
        tracer_bullet_template = f"""
        from flask import Flask, jsonify
        app = Flask(__name__)
        @app.{method}('{route}')
        def home():
            return jsonify({response}), 200
        if __name__ == "__main__":
            app.run(debug=True)
        """
        tracer_bullet_filename = "tracer_bullet.py"
        return self.create_file_from_template(tracer_bullet_template, tracer_bullet_filename)

if __name__ == "__main__":
    pp_agent = PragmaticProgrammerAGIAgent()
    docker_compose_file = pp_agent.create_docker_compose_file()
    pytest_file = pp_agent.create_pytest_file(funcs=['func1', 'func2', 'func3'])
    git_action_file = pp_agent.create_git_action_file()
    tracer_bullet_file = pp_agent.tracer_bullet_implementation(route="/", method="route", response='"Hello, World!"')
    for file in [docker_compose_file, pytest_file, git_action_file, tracer_bullet_file]:
        pp_agent.add_commit_push(filename=file, message=f"Added {file}")
```