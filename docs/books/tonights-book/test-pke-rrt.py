import numpy as np
import matplotlib.pyplot as plt
from PathPlanning.RRT import RRT
from PKE import PKE

def run_pke_rrt_test(n_goals, complex_scenario):
    """
    This function conducts the PKE-RRT algorithm test for complex multi-goal path finding.

    Args:
    n_goals (int): Number of goals.
    complex_scenario (Scenario): The complex scenario to run the test on.

    Returns:
    dict: The test result including time taken, path length and memory used.
    """

    # Initialize the PKE algorithm
    pke_algorithm = PKE()

    # Initialize the RRT algorithm
    rrt_algorithm = RRT()

    # Set the scenario
    pke_algorithm.set_scenario(complex_scenario)
    rrt_algorithm.set_scenario(complex_scenario)

    # Set the number of goals
    pke_algorithm.set_goals(n_goals)
    rrt_algorithm.set_goals(n_goals)

    # Run the PKE-RRT algorithm and measure performance
    test_result = pke_algorithm.run_rrt(rrt_algorithm)

    return test_result

# Define the complex scenario
complex_multi_goal_scenario = Scenario()

# Set the number of goals
n_goals = 10

# Run the PKE-RRT test for the scenario with multiple goals
test_result = run_pke_rrt_test(n_goals, complex_multi_goal_scenario)

# Print the test result
print(f"Time Taken: {test_result['time_taken']}s, Path Length: {test_result['path_length']}, Memory Used: {test_result['memory_used']}MB")

# Plot the results
plt.figure()
plt.plot(test_result['time_taken'], test_result['path_length'], label='Path Length')
plt.plot(test_result['time_taken'], test_result['memory_used'], label='Memory Used')
plt.xlabel('Time Taken (s)')
plt.ylabel('Path Length / Memory Used (MB)')
plt.legend()
plt.title('PKE-RRT Algorithm Performance in Complex Multi-Goal Path Finding Scenarios')
plt.show()
