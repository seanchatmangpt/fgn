import matplotlib.pyplot as plt
import networkx as nx
import os
import yaml
import pytest
from collections import deque, namedtuple
from typing import Dict, List, Union
from dataclasses import dataclass
from faker import Faker


def create_weighted_graph(code_components: Dict) -> nx.DiGraph:
    """
    Creates a weighted directed graph from provided dictionary.

    :param code_components: A dictionary representing code components and their dependencies
    :return: A weighted directed graph
    """
    graph = nx.DiGraph()
    for component, relations in code_components.items():
        for relation, cost in relations:
            graph.add_edge(component, relation, weight=cost)
    return graph


def visualize_weighted_graph(graph: nx.DiGraph):
    """
    Visualizes a provided weighted directed graph.

    :param graph: Weighted directed graph to visualize
    """
    weights = nx.get_edge_attributes(graph, 'weight')
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='r')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)
    plt.show()


@dataclass
class ComplexMultiLineTemplate:
    class_name: str
    attributes: List[namedtuple]
    methods: List[namedtuple]

    def render(self) -> str:
        """
        Renders a code template according to the provided attributes and methods.

        :return: The rendered template code as a string
        """
        faker = Faker()
        code = f"class {self.class_name}:\n"
        # Define the initializer
        code += "    def __init__(self"
        for attr in self.attributes:
            code += f", {attr.name}: {attr.type}"
        
        code += "):\n"
        for attr in self.attributes:
            code += f"        self.{attr.name} = {attr.name}\n"
        
        # Define the methods
        for method in self.methods:
            code += f"\n    def {method.name}(self"
            for param in method.params:
                code += f", {param.name}: {param.type}"
            
            # Adding a faker sentence to simulate logic in the methods
            code += f"):\n        return \"{faker.sentence()}\"\n"

        return code


@pytest.fixture
def rendered_complex_multiline_template() -> str:
    faker = Faker()
    attributes = [Attribute(name=faker.word(), type=faker.word()) for _ in range(3)]
    methods = [
        Method(
            name=faker.word(),
            params=[Param(name=faker.word(), type=faker.word()) for _ in range(2)],
        )
        for _ in range(3)
    ]

    template = ComplexMultiLineTemplate(
        class_name=faker.word().capitalize(), attributes=attributes, methods=methods
    )

    rendered_template = template.render()
    return rendered_template


class ProjectManagerAgent:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.project_config = self.load_yaml()

    def load_yaml(self) -> Dict:
        with open(self.yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        return config['pke']

    def extract_components(self, key: str) -> Dict:
        return self.project_config[key]

    def prioritize_tasks(self) -> List[str]:
        task_dependencies = self.extract_components('task_dependencies')
        promising_regions = self.extract_components('promising_regions')
        guidelines = self.extract_components('guidelines')
        heuristics = self.extract_components('heuristics')

        tasks_queue = deque()
        for task, dependencies in task_dependencies.items():
            if all(dep in promising_regions for dep in dependencies) and task in guidelines:
                tasks_queue.append((heuristics.get(task, 0), task))

        tasks_queue = sorted(tasks_queue, key=lambda x: x[0], reverse=True)
        return [task[1] for task in tasks_queue]

    def estimate_completeness(self, source_directory: str) -> float:
        total_lines = 0
        completed_lines = 0
        for root, _, files in os.walk(source_directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as code_file:
                        lines = code_file.readlines()
                        total_lines += len(lines)
                        completed_lines += sum(1 for line in lines if line.strip())

        completeness_percentage = (completed_lines / total_lines) * 100 if total_lines > 0 else 0
        return completeness_percentage


# Usage
project_config_file = 'project_config.yaml'
project_directory = '/path/to/full_stack_project'

project_manager = ProjectManagerAgent(project_config_file)

# Define task descriptions 
task_descriptions = ["Backend API", "Frontend UI", "Database Setup", "User Authentication", "Deployment"]
prompts = [f"Create code for: {task}" for task in task_descriptions]

# Add code to generate and save code for each task
