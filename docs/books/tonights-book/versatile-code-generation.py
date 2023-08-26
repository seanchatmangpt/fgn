import random
import numpy as np
from scipy.spatial import distance
import unittest

# Node class represents each point on our path
class Node:
    def __init__(self, coordinates):
        self.coordinates = np.array(coordinates)  # Convert coordinates to numpy array for easier computation
        self.parent = None  # Initialise parent as None. This will be updated as the path is formed


# PathFindingTree represents the entire path from start to goal as a tree of Nodes
class PathFindingTree:
    def __init__(self, start, goal):
        self.start = Node(start)  # Start Node of the path
        self.goal = Node(goal)  # Goal Node of the path
        self.nodes = [self.start]  # List to store all Node's in the path 

    def add_node(self, node):  
        self.nodes.append(node)  # Adding new Node to the path tree


# PKERRT represents the path finding algorithm
class PKERRT:
    def __init__(self, start, goal, obstacle_list, size):
        self.start = np.array(start)  # Start Node of the path
        self.goal = np.array(goal)  # Goal Node of the path
        self.size = size  # Size of the environment (Here it's a 2D grid)
        self.obstacle_list = obstacle_list  # List of all obstacles in the 2D grid

        self.tree = PathFindingTree(self.start, self.goal)  # Initialise the path as a PathFindingTree object

    def plan(self):
        while True:
            random_node = self.get_random_node()  # Get random Node
            nearest_node = self.get_nearest_node(random_node)  # Get nearest Node from the random Node

            new_node = self.move_towards(nearest_node, random_node)  # Get new Node by moving from nearest Node to random Node

            if self.check_collision(new_node):  # If there is a collision, continue to next iteration
                continue

            self.tree.add_node(new_node)  # If no collision, add the new Node to the tree

            if distance.euclidean(new_node.coordinates, self.goal) < 1.0:  # If the new Node is close to the goal, return the entire path
                return self.get_path(new_node)

    def get_random_node(self):
        return Node(np.array([random.uniform(0, self.size), random.uniform(0, self.size)]))  # Return a random Node within our 2D grid

    def get_nearest_node(self, node):
        distances = [distance.euclidean(n.coordinates, node.coordinates) for n in self.tree.nodes]  # Calculate distance of 'node' from all nodes in our tree path
        nearest_index = np.argmin(distances)  # Get index of the nearest Node
        return self.tree.nodes[nearest_index]  # Return the nearest Node

    def move_towards(self, nearest_node, random_node):
        direction = (random_node.coordinates - nearest_node.coordinates) / np.linalg.norm(random_node.coordinates - nearest_node.coordinates)  # Calculate the direction from nearest Node to random Node
        new_node = Node(nearest_node.coordinates + direction)  # Create new Node in this direction
        new_node.parent = nearest_node  # Set parent of new Node to the nearest Node

        return new_node  # Return the new Node

    def check_collision(self, node):
        for ob in self.obstacle_list:  # Loop through all obstacles
            if distance.euclidean(node.coordinates, ob) < 1.0:  # If Node is within 1.0 distance of any obstacle, return True (collision)
                return True
        return False  # If loop completes without returning, means no collision. Return False.

    def get_path(self, node):
        path = []
        while node is not None:  # Start from goal and go to start by going to parent at each step
            path.append(node.coordinates)  # Add node coordinates to the path
            node = node.parent  # Go to the next node (parent)

        return path  # Return the path


class TestPkerrt(unittest.TestCase):
    def setUp(self):
        obstacle_list = [[2, 2], [3, 3], [4, 4], [5, 5]]  # Set up any test obstacles
        self.pkerrt = PKERRT(start=[0, 0], goal=[6, 6], obstacle_list=obstacle_list, size=10)  # Initialize pkerrt with start, end, obstacles and grid size = 10

    def test_get_random_node(self):
        node = self.pkerrt.get_random_node()  # Get a random node
        self.assertEqual(len(node.coordinates), 2)  # Test that it has 2 coordinates
        self.assertTrue(
            0 <= node.coordinates[0] <= self.pkerrt.size and 0 <= node.coordinates[1] <= self.pkerrt.size  # Test that its coordinates are within the grid size
        )

    def test_get_nearest_node(self):
        node = self.pkerrt.get_random_node()  # Get a random node
        nearest_node = self.pkerrt.get_nearest_node(node)  
        for n in self.pkerrt.tree.nodes:
            self.assertTrue(  # For all Nodes in the path tree, check that none of them are closer than the 'nearest_node' we got
                distance.euclidean(nearest_node.coordinates, node.coordinates) <= distance.euclidean(n.coordinates, node.coordinates)
            )


if __name__ == "__main__":
    unittest.main()  # Run unit tests
