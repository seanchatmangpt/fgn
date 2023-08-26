import random
import numpy as np
from scipy.spatial import distance
import unittest

class Node:
    """
    Class to represent a node in the path finding tree.
    """
    def __init__(self, coordinates):
        """
        Initialize a Node instance.

        :param coordinates: The x and y coordinates of the node
        """
        self.coordinates = np.array(coordinates)
        self.parent = None

class PathFindingTree:
    """
    Class to represent the path finding tree for the PKE-RRT algorithm.
    """
    def __init__(self, start, goal):
        """
        Initialize a PathFindingTree instance.

        :param start: The starting point of the path
        :param goal: The goal point of the path
        """
        self.start = Node(start)
        self.goal = Node(goal)
        self.nodes = [self.start]

    def add_node(self, node):
        """
        Adds a node to the path finding tree.

        :param node: The node to add
        """
        self.nodes.append(node)

class PKERRT:
    """
    Class to represent the PKE-RRT algorithm.
    """
    def __init__(self, start, goal, obstacle_list, size):
        """
        Initialize a PKERRT instance.

        :param start: The starting point of the path
        :param goal: The goal point of the path
        :param obstacle_list: A list of obstacles in the path
        :param size: The size of the environment
        """
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.size = size
        self.obstacle_list = obstacle_list
        self.tree = PathFindingTree(self.start, self.goal)

    def plan(self):
        """

        """
        while True:
            random_node = self.get_random_node()
            nearest_node = self.get_nearest_node(random_node)
            new_node = self.move_towards(nearest_node, random_node)

            if self.check_collision(new_node):
                continue

            self.tree.add_node(new_node)

            if distance.euclidean(new_node.coordinates, self.goal) < 1.0:
                return self.get_path(new_node)

    def get_random_node(self):
        """
        """
        return Node(np.array([random.uniform(0, self.size), random.uniform(0, self.size)]))

    def get_nearest_node(self, node):
        """
        """
        distances = [distance.euclidean(n.coordinates, node.coordinates) for n in self.tree.nodes]
        nearest_index = np.argmin(distances)
        return self.tree.nodes[nearest_index]

    def move_towards(self, nearest_node, random_node):
        """
        """
        direction = (random_node.coordinates - nearest_node.coordinates) / np.linalg.norm(random_node.coordinates - nearest_node.coordinates)
        new_node = Node(nearest_node.coordinates + direction)
        new_node.parent = nearest_node
        return new_node

    def check_collision(self, node):
        """
        """
        for ob in self.obstacle_list:
            if distance.euclidean(node.coordinates, ob) < 1.0:
                return True
        return False

    def get_path(self, node):
        """
        """
        path = []
        while node is not None:
            path.append(node.coordinates)
            node = node.parent
        return path


class TestPkerrt(unittest.TestCase):
    """
    Unit tests for the PKERRT class
    """
    def setUp(self):
        obstacle_list = [[2, 2], [3, 3], [4, 4], [5, 5]]
        self.pkerrt = PKERRT(start=[0, 0], goal=[6, 6], obstacle_list=obstacle_list, size=10)

    def test_get_random_node(self):
        """
        Test for get_random_node method
        """
        node = self.pkerrt.get_random_node()
        self.assertEqual(len(node.coordinates), 2)
        self.assertTrue(
            0 <= node.coordinates[0] <= self.pkerrt.size and 0 <= node.coordinates[1] <= self.pkerrt.size
        )

    def test_get_nearest_node(self):
        """
        Test for get_nearest_node method
        """
        node = self.pkerrt.get_random_node()
        nearest_node = self.pkerrt.get_nearest_node(node)
        for n in self.pkerrt.tree.nodes:
            self.assertTrue(
                distance.euclidean(nearest_node.coordinates, node.coordinates) <= distance.euclidean(n.coordinates, node.coordinates)
            )


if __name__ == "__main__":
    unittest.main()
