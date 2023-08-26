import matplotlib.pyplot as plt
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

# To visualize the graph, you can use the following function
def visualize_weighted_graph(graph):
    weights = nx.get_edge_attributes(graph, 'weight')
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='r')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)

code_components = {
    "component1": [("component2", 1.5), ("component5", 2.0)],
    "component2": [("component3", 1.0)],
    "component3": [("component4", 0.5)],
    "component5": [("component1", 0.8), ("component4", 1.6)]
}

graph = create_weighted_graph(code_components)

# To visualize the graph
visualize_weighted_graph(graph)
