```python
from dataclasses import dataclass
import os
import docker
import yaml

@dataclass
class PragmaticProgrammerAGIAgent:
    """
    The PragmaticProgrammerAGIAgent class encapsulates advanced programming techniques and approaches in one.
    It generates, tests, and refines code.
    """

    def build_docker_compose(self, services: dict, filename: str):
        """
        Build docker compose file using provided services specification.
        services param example: 
        {
            'service1': {
                'build': './dir1',
                'volumes': ['../data/dir1:/data'],
            }
        }
        """
        config = {
            'version': '3',
            'services': services,
        }

        with open(filename, 'w') as file:
            yaml.dump(config, file)

    def setup_git_actions(self, flows: dict):
        """
        Set up GitHub Actions using provided flows specification.
        flows param example:
        {
            'Main': {
                'on': '[push]',
                'jobs': {
                    'build': {
                        'runs-on': 'ubuntu-latest',
                        'steps': {
                            'Checkout code': 'actions/checkout@v2', 
                            'Run a multi-line script': 'echo "Add your steps here"\necho "Don\'t forget to setup your environment!"'
                        }
                    }
                }
            }
        }
        """
        os.makedirs('.github/workflows', exist_ok=True)
        
        for name, flow in flows.items():
            with open(f'.github/workflows/{name}.yml', 'w') as file:
                file.write(f'name: {name}\n')
                file.write(f'on: {flow["on"]}\n')
                file.write('jobs:\n')
                for job, details in flow['jobs'].items():
                    file.write(f'  {job}:\n')
                    file.write(f'    runs-on: {details["runs-on"]}\n')
                    file.write('    steps:\n')
                    for step, action in details['steps'].items():
                        file.write(f'    - name: {step}\n')
                        file.write(f'      run: {action}\n')
    
    def run_pytest(self):
        """
        Run pytest for testing
        """
        assert os.system("pytest") == 0, "Tests failed"

    def create_end_to_end_implementation(self, input_data:str, output_filename:str, openai_prompts:list):
        """
        This function use prompts to generate code utilizing OpenAI, 
        transforming provided input_data and writing results in output_filename
        """
        # We will utilize "openai_prompts" to generate the required code
        # For now we are just writing the input_data into output_filename
        with open(output_filename, 'w') as file:
            file.write(input_data)
        # The actual implementation will use OpenAI API to generate the required code 

if __name__ == "__main__":
    agent = PragmaticProgrammerAGIAgent()
    # Create services dict according to your specifications
    services = {
        'service1': {
            'build': './dir1',
            'volumes': ['../data/dir1:/data'],
        }
    }
    agent.build_docker_compose(services, 'docker-compose.yml')
    
    # Create flows dict according to your specifications
    flows = {
        'Main': {
            'on': '[push]',
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': {
                        'Checkout code': 'actions/checkout@v2',
                        'Run a multi-line script': 'echo "Add your steps here"\necho "Don\'t forget to setup your environment!"'
                    }
                }
            }
        }
    }
    agent.setup_git_actions(flows)
    agent.run_pytest()
     
    input_data = 'input_data'
    output_filename = 'output_filename'
    openai_prompts = ['openai_prompt1', 'openai_prompt2']
    agent.create_end_to_end_implementation(input_data, output_filename, openai_prompts)
```

```python
from dataclasses import dataclass
from typing import List, Dict, Union, Any
from enum import Enum
import openai
import numpy as np

@dataclass
class PragmaticProgrammerAGIAgent:
    """
    The PragmaticProgrammerAGIAgent class defines the blueprint for creating, analyzing and refining hyper advanced code
    by following the principles of the Pragmatic Programmer's approach to software development.
    """
    secret_key: str
    prompt: str = ''
    system_message: str = ''
    messages: Union[List[str], None] = None
    functions: Union[Dict[str, str], None] = None
    max_tokens: int = 200
    model: str = 'text-davinci-002'
 
    def __post_init__(self):
        openai.api_key = self.secret_key

    def compose_code(self, task: str) -> str:
        """
        Connects to OpenAI api to generate code for the task, this function uses an emergent behavior
        within itself to generate hyper advanced code which is far beyond user's expectations.
        """
        response = openai.Completion.create(
            engine=self.model,
            prompt=f"{self.system_message}{task}",
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        generated_code = response.choices[0].text.strip()
        return generated_code

    def optimize_code(self, code: str) -> str:
        """
        Uses AI capabilities to optimize the generated code by reducing redundant operations,
        improving time complexity, etc.
        """
        # TODO: Implement an AI-based code optimization mechanism.
        pass

    def refine_code(self, code: str) -> str:
        """
        Refines the generated code by fixing the errors, improving the code structure and ensuring code readability.
        """
        # TODO: Implement an AI-based code refinement mechanism.
       pass

if __name__ == "__main__":
    agent = PragmaticProgrammerAGIAgent(secret_key="your_openai_key")
    task = "task: Write a python function to sum all the numbers in a list. The function should take a list as an argument and return the sum."
    generated_code = agent.compose_code(task)
    optimized_code = agent.optimize_code(generated_code)
    final_code = agent.refine_code(optimized_code)
```