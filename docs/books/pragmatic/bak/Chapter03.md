```python
from dataclasses import dataclass
import os
import docker
import yaml
import pytest

@dataclass
class PragmaticProgrammerAGIAgent:
    """
    The PragmaticProgrammerAGIAgent creates hyper-advanced systems by combining state-of-the-art software development methodologies such
    as Domain-Driven Design (DDD), docker compose, git actions, pytest, file system I/O, and uses OpenAI to generate system files.
    """

    def build_docker_compose(self, services: dict, filename: str):
        """
        Create a docker compose file using the provided services specification.
        """
        config = {
            'version': '3',
            'services': services,
        }
        with open(filename, 'w') as file:
            yaml.dump(config, file)

    def setup_git_actions(self, flows: dict):
        """
        Create GitHub Actions workflows.
        """
        os.makedirs('.github/workflows', exist_ok=True)
        for name, flow in flows.items():
            with open(f'.github/workflows/{name}.yml', 'w') as file:
                yaml.dump({name: flow}, file)

    def run_pytest(self):
        """
        Run pytest for testing.
        """
        assert pytest.main([]) == 0, "Tests failed"

    def create_end_to_end_implementation(self, input_data:str, output_filename:str, openai_prompts:list):
        """
        Create an end-to-end Tracer Bullet implementation that can read and write from the filesystem. The implementation will 
        use OpenAI API to generate the necessary code.
        """
        # Code generation using OpenAI API goes here.
        implemented_code = self.openai_completion(openai_prompts)
        with open(output_filename, 'w') as file:
            file.write(implemented_code)

    def openai_completion(self, openai_prompts):
        """
        Interact with the OpenAI API to generate system files.
        For the purpose of this demo, it just returns a concatenation of the openai_prompts.
        """
        # Code to interact with OpenAI API goes here.
        return "\n".join(openai_prompts)

if __name__ == "__main__":
    agent = PragmaticProgrammerAGIAgent()
    # Setup services for docker
    services = {
        'service1': {
            'build': './dir1',
            'volumes': ['../data:/data'],
        }
    }
    agent.build_docker_compose(services, 'docker-compose.yml')
    
    # Setup workflows for Github Actions
    flows = {
        'Main': {
            'on': ['push'],
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [{'name': 'Checkout', 'uses': 'actions/checkout@v2'}]
                }
            }
        }
    }
    agent.setup_git_actions(flows)
    
    # Run tests
    agent.run_pytest()
     
    # Create end-to-end implementation
    input_data = 'raw_input'
    output_filename = 'output.py'

    # Generate code using openai prompts
    openai_prompts = ['import os', 'def read_file(file_path):\n\treturn open(file_path).read()']
    agent.create_end_to_end_implementation(input_data, output_filename, openai_prompts)
```