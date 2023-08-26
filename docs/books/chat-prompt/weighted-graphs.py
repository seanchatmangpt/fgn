import networkx as nx

def create_weighted_graph(code_components):
    """
    This function generates a weighted graph from the given code components.
    Nodes of the graph represent code components and edges represent the relationship between them.
    The weight on the edges represent the 'distance' or 'cost' between two components.
    
    :param code_components: A dictionary with component names as keys and a list of related components and their costs as values
    :return: A weighted graph representing the code components and their relationships
    """
    graph = nx.Graph()

    for component, relations in code_components.items():
        for relation, cost in relations:
            graph.add_edge(component, relation, weight=cost)

    return graph

# Usage
code_components = {
    "component1": [("component2", 1.5), ("component5", 2.0)],
    "component2": [("component3", 1.0)],
    "component3": [("component4", 0.5)],
    "component5": [("component1", 0.8), ("component4", 1.6)]
}

graph = create_weighted_graph(code_components)

import unittest

class TestCodeComponents(unittest.TestCase):
    def test_create_weighted_graph(self):
        code_components = {
        "component1": [("component2", 1.5), ("component5", 2.0)],
        "component2": [("component3", 1.0)],
        "component3": [("component4", 0.5)],
        "component5": [("component1", 0.8), ("component4", 1.6)]
        }
        graph = create_weighted_graph(code_components)
        self.assertEqual(len(graph.nodes), 5)
        self.assertEqual(len(graph.edges), 5)

if __name__ == '__main__':
    unittest.main()
