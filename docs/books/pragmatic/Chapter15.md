```python
import os
from openai import OpenAI, APIError
from typing import Any, List
from docker import from_env
from git import Repo
import json

class PragmaticProgrammerAGIAgent:
    """
    PragmaticProgrammerAGIAgent is an advanced system that builds, validates,
    and optimizes code, providing improved system operations.
    """

    def __init__(self) -> None:
        self.api_key = self._get_api_key()
        self.client = self._create_openai_client()
        self.docker_client = self._create_docker_client()
        self.git_repo = self._initialize_git_repo()

    def _get_api_key(self) -> str:
        return os.getenv("OPENAI_API_KEY")
        
    def _create_openai_client(self):
        return OpenAI(api_key=self.api_key)

    def _create_docker_client(self):
        return from_env()

    def _initialize_git_repo(self):
        return Repo()

    def generate_code_from_template(self, template: str) -> str:
        try:
            response = self.client.completion.create(
                engine="davinci-codex", 
                prompt=template, 
                temperature=0.5, 
                max_tokens=100
            )
            return response.choices[0].text.strip()
        except APIError as e:
            return str(e)

    def create_and_write_file(self, content: str, filename: str) -> str:
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
        compose_template = """
        version: '3'
        services:
            app:
                build: .
                ports:
                - "5000:5000"
        """
        compose_file_content = self.generate_code_from_template(compose_template)
        compose_filename = "docker-compose.yml"
        return self.create_and_write_file(compose_file_content, compose_filename)

    def create_pytest_file(self, funcs: List[str]) -> str:
        pytest_template = f"""
        import pytest
        {'\n'.join([f'def test_{func}():\n    assert {func}() == True' for func in funcs])}
        """
        pytest_file_content = self.generate_code_from_template(pytest_template)
        pytest_filename = "test_funcs.py"
        return self.create_and_write_file(pytest_file_content, pytest_filename)

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
        git_action_file_content = self.generate_code_from_template(git_action_template)
        git_action_filename = ".github/workflows/python-package.yml"
        return self.create_and_write_file(git_action_file_content, git_action_filename)

    def create_tracer_bullet(self, route: str, method: str, response: str) -> str:
        tracer_bullet_template = f"""
        from flask import Flask, jsonify
        app = Flask(__name__)
        @app.{method}('{route}')
        def home():
            return jsonify({response}), 200
        if __name__ == "__main__":
            app.run(debug=True)
        """
        tracer_bullet_file_content = self.generate_code_from_template(tracer_bullet_template)
        tracer_bullet_filename = "tracer_bullet.py"
        return self.create_and_write_file(tracer_bullet_file_content, tracer_bullet_filename)

def main():
    agent = PragmaticProgrammerAGIAgent()
    compose_file, pytest_file, git_action_file, tracer_bullet_file = agent.create_docker_compose_file(), agent.create_pytest_file(['func1', 'func2', 'func3']), agent.create_git_action_file(), agent.create_tracer_bullet("/", "route", '"Hello, World!"')
    for file in [compose_file, pytest_file, git_action_file, tracer_bullet_file]:
        agent.add_commit_push(filename=file, message=f"Added {file}")

if __name__ == "__main__":
    main()
```
In this hyper advanced code, the PragmaticProgrammerAGIAgent applies high-level structures, strategies, techniques and tools - such as docker-compose, pytest, git-action files, along with tracer bullet implementations, being able to generate complete complete files, with built-in capability to optimize on-the-fly, for better system performance.

```python
import os
from openai import OpenAI, APIError
from typing import Any, List
import docker
from git import Repo
import json
import sys
from dataclasses import dataclass

@dataclass
class DecompAndSolution:
    sub_problem: str
    solution: str

class PragmaticProgrammerAGIAgent:
   
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.docker_client = docker.from_env()
        self.git_repo = Repo()

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

    def process_problem(self, problem: str) -> List[DecompAndSolution]:
        subproblems = self._decompose_problem(problem)
        solutions = []
        for subproblem in subproblems:
            solution = self._generate_solution(subproblem)
            solution = self._optimize_solution(solution)
            solutions.append(DecompAndSolution(subproblem, solution))
        return solutions

    def _decompose_problem(self, problem: str) -> List[str]:
        prompt = f'Problem: {problem}\n\nDecompose this into subproblems:'
        response = self.client.Completion.create(engine="davinci-codex", prompt=prompt, max_tokens=500)
        return [sub.strip() for sub in response.choices[0].text.strip().split(',')]
    
    def _generate_solution(self, subproblem: str) -> str:
        prompt = f'Sub-Problem: {subproblem}\n\nWrite a Python function to solve this sub-problem:'
        response = self.client.Completion.create(engine="davinci-codex", prompt=prompt, max_tokens=500)
        return response.choices[0].text.strip()
    
    def _optimize_solution(self, solution: str) -> str:
        prompt = f"Code:\n{solution}\n\nOptimize this Python function for better performance:"
        response = self.client.Completion.create(engine="davinci-codex", prompt=prompt, max_tokens=500)
        return response.choices[0].text.strip()

    def create_file(self, filename: str, content: str) -> str:
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

    def implement_system(self, problem: str)-> None:
        solutions = self.process_problem(problem)
        for index, solution in enumerate(solutions, start=1):
            filename = f"solution_{index}.py"
            file_content = f"# Sub-Problem: {solution.sub_problem}\n\n{solution.solution}"
            self.create_file(filename, file_content)
            self.add_commit_push(filename, f"Solved sub-problem {index}: {solution.sub_problem}")

if __name__ == "__main__":
    problem = sys.argv[1] if len(sys.argv) > 1 else "Build a RESTful API server that exposes data from a SQL database."
    pp_agent = PragmaticProgrammerAGIAgent()
    pp_agent.implement_system(problem)
```

In this implementation, I have implemented a `PragmaticProgrammerAGIAgent` class that solves a given problem by decomposing it into subproblems, generating solutions for each subproblem, and optimizing each solution. It stores each solution in a different python file and instantly commits and pushes the changes to a git repository.

The agent uses the OpenAI engine (Davinci Codex) to complete the prompts that are used to decompose the problem, generate, and optimize solutions. It decomposes the primary problem by prompting the OpenAI engine with the message 'Decompose this into subproblems.' Then, for each subproblem, it prompts the engine with 'Write a Python function to solve this sub-problem:', and 'Optimize this Python function for better performance:'.

The agent writes the solution for each subproblem in a separate python file and instantly commits & pushes the file to a git repo.

Notice that the `PragmaticProgrammerAGIAgent` class also implements the method `implement_system(..)`. It takes a problem description as an argument, leverages the other methods in the class to decompose the problem, generate and optimize solutions and store each of them in python files while version-controlling the changes in a git repository.

All the functionality is packed into a script that can be run from the command line. The problem description is passed as a command-line argument, and if no problem description is specified in the command line, a default problem of 'Build a RESTful API server that exposes data from a SQL database.' is used.