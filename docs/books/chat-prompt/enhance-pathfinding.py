import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import os
import yaml
from typing import Dict, List, Union
from faker import Faker
from collections import namedtuple
from dataclasses import dataclass
import pytest

def create_weighted_graph(code_components):
    graph = nx.Graph()
    for component, relations in code_components.items():
        for relation, cost in relations:
            graph.add_edge(component, relation, weight=cost)
    return graph

def visualize_weighted_graph(graph):
    weights = nx.get_edge_attributes(graph, 'weight')
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='r')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)

# To create and visualize the weighted graph
code_components = {
    "component1": [("component2", 1.5), ("component5", 2.0)],
    "component2": [("component3", 1.0)],
    "component3": [("component4", 0.5)],
    "component5": [("component1", 0.8), ("component4", 1.6)]
}

graph = create_weighted_graph(code_components)
visualize_weighted_graph(graph)
plt.show()

# The class below is used to manage multi-goal projects by prioritizing tasks and estimating project completeness
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

    def plan_full_stack_project(self, project_directory: str):
        prioritized_tasks = self.prioritize_tasks()
        task_descriptions = self.generate_task_descriptions()

        for task_description in task_descriptions:
            prompt = f"Create code for: {task_description}"
            final_code = chat(prompt=prompt, sys_msg="Your system message here")

            task_file_path = os.path.join(project_directory, f"{task_description.lower().replace(' ', '_')}.py")
            with open(task_file_path, 'w') as task_file:
                task_file.write(final_code)
            print(f"Generated code for {task_description}")

        print("Project code generation complete.")

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
