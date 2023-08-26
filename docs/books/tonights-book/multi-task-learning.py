import time
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple

import unittest

from pkerrrt import PKE_RRT
from environment import Environment


class PerformanceTesting:
    """
    The PerformanceTesting class is responsible for testing the performance of 
    PKE-RRT Algorithm in complex multi-goal path finding scenarios.

    Attributes:
        env (Environment): The test environment.
        algorithm (PKE_RRT): The algorithm to be tested.
    """

    def __init__(self, env: Environment, algorithm: PKE_RRT):
        """
        Initialize a new instance of PerformanceTesting.

        Args:
            env (Environment): The test environment.
            algorithm (PKE_RRT): The algorithm to be tested.
        """
        self.env = env
        self.algorithm = algorithm

    def run_tests(self, test_scenarios: List[Tuple[List, int]], 
                  num_runs: int = 5) -> pd.DataFrame:
        """
        Runs the specified test scenarios for a number of runs and records the average time taken.

        Args:
            test_scenarios (List[Tuple[List,int]]): A list of test scenarios. Each scenario is a tuple,
                                                    where first element is a list of goal points and second 
                                                    element is the number of additional targets to be added. 
            num_runs (int, optional): The number of times to run each scenario. Defaults to 5.

        Returns:
            pd.DataFrame: A DataFrame with the average time taken for each scenario.
        """
        # Initialize a dictionary to store the results
        results = {'scenario': [], 'avg_time': []}

        # Loop through each scenario
        for i, scenario in enumerate(test_scenarios):
            print(f"Running Scenario {i+1}...")

            # Initialize total time to 0
            total_time = 0

            # Run the scenario for the specified number of runs
            for _ in range(num_runs):
                start_time = time.time()
                self.algorithm.execute(scenario[0], scenario[1])
                end_time = time.time()
                total_time += (end_time - start_time)

            # Compute the average time
            avg_time = total_time / num_runs

            # Record the result
            results['scenario'].append(i+1)
            results['avg_time'].append(avg_time)

        return pd.DataFrame(results)


def plot_results(df: pd.DataFrame):
    """
    Plots the provided results.

    Args:
        df (pd.DataFrame): The DataFrame containing the testing results.
    """
    plt.bar(df['scenario'], df['avg_time'])
    plt.title("PKE-RRT Algorithm Performance")
    plt.xlabel("Scenario")
    plt.ylabel("Average Time")
    plt.show()


if __name__ == "__main__":
    # Initialize the test environment and the PKE-RRT algorithm
    env = Environment()
    algorithm = PKE_RRT(env)

    # Define the test scenarios
    test_scenarios = [
        # Scenario 1: 5 goals, add 10 additional targets
        ([('A', 'B', 2.5), ('A', 'C', 5), ('B', 'D', 7.5), ('C', 'E', 10)], 10),

        # Scenario 2: 10 goals, add 20 additional targets
        ([('A', 'B', 2.5), ('A', 'C', 5), ('B', 'D', 7.5), ('C', 'E', 10)], 20)
    ]

    # Initialize the performance tester
    tester = PerformanceTesting(env, algorithm)

    # Run the tests and get the results
    results = tester.run_tests(test_scenarios)

    # Plot the results
    plot_results(results)
