class Node:
    """
    Node class represents a node in the graph with a unique identifier and a set of edges to other nodes.
    """
    def __init__(self, name):
        """
        Initializes a new instance of the Node class.

        Args:
            name (str): The unique identifier of the node.
        """
        self.name = name
        self.edges = {}

    def add_edge(self, node, cost):
        """
        Adds an edge from this node to another node with an associated cost.

        Args:
            node (Node): The node that the edge connects to.
            cost (float): The cost of traversing the edge.
        """
        self.edges[node] = cost

    def get_cost(self, node):
        """
        Gets the cost of the edge between this node and another node.

        Args:
            node (Node): The node that the edge connects to.
        
        Returns:
            float: The cost of the edge. Returns infinity if no direct edge exists.
        """
        return self.edges.get(node, float('inf'))


class Graph:
    """
    Graph class represents a graph data structure with nodes and the edges between them.
    """
    def __init__(self):
        """
        Initializes a new instance of the Graph class.
        """
        self.nodes = {}

    def add_node(self, name):
        """
        Adds a node to the graph.

        Args:
            name (str): The unique identifier of the node.
        """
        self.nodes[name] = Node(name)

    def add_edge(self, node_name1, node_name2, cost):
        """
        Adds an edge between two nodes in the graph with an associated cost.

        Args:
            node_name1 (str): The unique identifier of the first node.
            node_name2 (str): The unique identifier of the second node.
            cost (float): The cost of traversing the edge.
        """
        self.nodes[node_name1].add_edge(self.nodes[node_name2], cost)
        self.nodes[node_name2].add_edge(self.nodes[node_name1], cost)  # For undirected graph

    def get_cost(self, node_name1, node_name2):
        """
        Gets the cost of the edge between two nodes.

        Args:
            node_name1 (str): The unique identifier of the first node.
            node_name2 (str): The unique identifier of the second node.
        
        Returns:
            float: The cost of the edge. Returns infinity if no direct edge exists.
        """
        return self.nodes[node_name1].get_cost(self.nodes[node_name2])   

# This is a code skeleton for performing multi-goal path finding with dynamic graph heuristics.
# To fully implement this, you will need an AGI that can understand your project's specifications and constraints.
# The AGI will then generate a tailored implementation for your project.
