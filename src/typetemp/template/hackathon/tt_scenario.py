# Here is your PerfectProductionCode® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

from dataclasses import dataclass

from typetemp.template.typed_template import TypedTemplate


@dataclass
class TypedScenarioTemplate(TypedTemplate):
    """
    Class to represent a single BDD scenario template. This will be used
    as part of the TypedBDDTestFactory to build each scenario.
    """

    name: str
    given: str
    when: str
    then: str
    source: str = "Scenario: {{ name }}\n  Given {{ given }}\n  When {{ when }}\n  Then {{ then }}"


# Sample usage
if __name__ == "__main__":
    from src.typetemp.template.hackathon.tt_bdd import TypedBDDTestFactory

    scenarios_data = [
        {
            "name": "Implement Function Creation",
            "given": 'the user asks "Create a function to calculate factorial"',
            "when": "the agent processes the request",
            "then": "it should return a syntactically correct Python function for calculating factorial",
        },
        {
            "name": "CLI Game Development",
            "given": 'the user asks "Develop a CLI-based Tic-Tac-Toe game"',
            "when": "the agent processes the request",
            "then": "it should return a functional CLI Tic-Tac-Toe game in Python",
        }
        # Add more scenarios here
    ]

    typed_scenarios = [TypedScenarioTemplate(**scenario) for scenario in scenarios_data]

    bdd_test_factory = TypedBDDTestFactory(
        project_name="Coding Excellence Agent",
        target_directory="/path/to/tests",
        repo_url="https://github.com/AutoGPT/AutoGPT-Project",
        scenarios=typed_scenarios,
        feature_name="Coding Excellence in AI Agents",
    )

    print(bdd_test_factory.generate_bdd_test())
