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