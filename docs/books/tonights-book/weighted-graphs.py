import networkx as nx

class CodeComponent:
    """
    Class to represent a component in a codebase or software application.
    """

    def __init__(self, name: str, weight: int):
        """
        Initializes a new CodeComponent instance.

        :param name: The name of the component.
        :param weight: The weight of the component representing its importance or complexity.
        """
        self.name = name
        self.weight = weight

class CodebaseGraph:
    """
    Class to represent a graph of code components in a codebase or software application.
    """

    def __init__(self):
        """
        Initializes a new CodebaseGraph instance.
        """
        self.graph = nx.Graph()

    def add_component(self, component: CodeComponent):
        """
        Adds a component to the graph.

        :param component: The component to add.
        """
        self.graph.add_node(component.name, weight=component.weight)

    def add_dependency(self, component1: CodeComponent, component2: CodeComponent):
        """
        Adds a dependency between two components.

        :param component1: The first component.
        :param component2: The second component.
        """
        self.graph.add_edge(component1.name, component2.name)

    def calculate_dependency_weight(self, component: CodeComponent) -> int:
        """
        Calculates the total weight of dependencies for a given component.

        :param component: The component for which to calculate the dependency weight.
        :return: The total weight of the component's dependencies.
        """

        if component.name in self.graph:
            dependencies = self.graph[component.name]
            return sum(self.graph.nodes[dep]['weight'] for dep in dependencies)
        else:
            return 0

# Test data
c1 = CodeComponent('c1', 10)
c2 = CodeComponent('c2', 20)
c3 = CodeComponent('c3', 30)

# Testing
codebase_graph = CodebaseGraph()
codebase_graph.add_component(c1)
codebase_graph.add_component(c2)
codebase_graph.add_component(c3)

codebase_graph.add_dependency(c1, c2)
codebase_graph.add_dependency(c2, c3)

print(codebase_graph.calculate_dependency_weight(c1))  # Should print 20
print(codebase_graph.calculate_dependency_weight(c2))  # Should print 40
