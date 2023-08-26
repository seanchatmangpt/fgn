# Import necessary libraries
import pytest
from faker import Faker
from collections import namedtuple
from dataclasses import dataclass
import tempfile
from jinja2 import Template
import openai
from typing import Optional, List
import logging

# Define the ComplexMultiLineTemplate class
@dataclass
class ComplexMultiLineTemplate(TypedTemplate):
    class_name: str
    attributes: list
    methods: list

    source = """class {{ class_name }}:
    def __init__(self{% for attr in attributes %}, {{ attr.name }}: {{ attr.type }}{% endfor %}):
        {% for attr in attributes -%}
        self.{{ attr.name }} = {{ attr.name }}
        {% endfor %}
    {%- for method in methods %}
    def {{ method.name }}(self{% for param in method.params %}, {{ param.name }}: {{ param.type }}{% endfor %}):
        return "{{ faker_sentence() }}"  # Simulating logic with Faker sentence{% endfor %}"""

# Define the pytest fixture for rendered_complex_multiline_template
@pytest.fixture
def rendered_complex_multiline_template():
    faker = Faker()
    Attribute = namedtuple('Attribute', ['name', 'type'])
    Method = namedtuple('Method', ['name', 'params'])
    Param = namedtuple('Param', ['name', 'type'])

    attributes = [Attribute(name=faker.word(), type=faker.word()) for _ in range(3)]
    methods = [Method(name=faker.word(), params=[Param(name=faker.word(), type=faker.word()) for _ in range(2)]) for _ in range(3)]

    template = ComplexMultiLineTemplate(class_name=faker.word().capitalize(), attributes=attributes, methods=methods)
    return template.render()

# Define the bool_prompt function
def bool_prompt(
    prompt: str,
    sys_msg: str = "A LLM 7 AGI Hive-Mind simulator",
    msgs: Optional[List[dict]] = None,
    funcs: Optional[List[dict]] = None,
    model: str = "gpt-3.5-turbo-0613",
    max_retry: int = 1,
    backoff_factor: int = 2,
    initial_wait: float = 0.25
) -> bool:
    """
    Customized completion function that interacts with the chat function, processing the response to return a boolean.
    """
    response = chat(
        prompt=prompt,
        sys_msg=sys_msg,
        msgs=msgs,
        funcs=funcs,
        model=model,
        max_retry=max_retry,
        backoff_factor=backoff_factor,
        initial_wait=initial_wait,
    )
    return response.lower() in ["yes", "true", "y", "t"]

# Define the Chat class
class Chat:
    def __init__(self, prompt: str = "Is it a good day today?", model: str = "gpt-3.5-turbo-0613"):
        self.prompt = prompt
        self.model = model

    def __call__(self) -> str:
        response = openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": self.prompt}])
        return response['choices'][0]['message']['content']

# Define the Agent class
class Agent:
    def __init__(self, name: str):
        self.name = name
        self.history = []

    def rap(self, opponent_name: str, prompt: str) -> str:
        """
        This method represents the rap action of the agent. It takes a prompt and returns a generated rap.
        """
        chat_instance = Chat(prompt=f"{self.name} vs {opponent_name}: {prompt}")
        rap_line = chat_instance()
        self.history.append(rap_line)
        return rap_line

    def judge(self, rap1: str, rap2: str, prompt: str) -> bool:
        """
        This method represents the judgment action of the agent. It takes two raps and a prompt to make a judgment.
        It returns a boolean representing the decision.
        """
        judgment_prompt = f"Judge the rap battle between two rappers:\nRap 1: {rap1}\nRap 2: {rap2}\n{prompt}"
        chat_instance = Chat(prompt=judgment_prompt)
        decision = bool_prompt(chat_instance)
        self.history.append(judgment_prompt)
        return decision


def rap_battle(agent1: Agent, agent2: Agent, judge: Agent, prompts: List[str]) -> None:
    """
    Simulates a rap battle between two agents and judged by the third.
    """
    for prompt in prompts:
        rap1 = agent1.rap(agent2.name, prompt)
        rap2 = agent2.rap(agent1.name, prompt)
        winner = judge.judge(rap1, rap2, f"Who won the battle? {judge.name}, make your judgment!")
        print(f"{agent1.name}: {rap1}\n{agent2.name}: {rap2}\nJudge {judge.name} says {'Agent 1' if winner else 'Agent 2'} wins this round!\n")

# Demo:
kool_keith = Agent(name="Kool Keith")
xzibit = Agent(name="Xzibit")
eminem = Agent(name="Eminem")

prompts = [
    "Round 1: Rap about your journey in the music industry.",
    "Round 2: Rap about your passion for hip-hop.",
    "Final Round: Rap about why you'll win this battle.",
]

rap_battle(kool_keith, xzibit, eminem, prompts)

# Set up the logging config
logging.basicConfig(level=logging.INFO)

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.history = []

    def rap(self, opponent_name: str, prompt: str) -> str:
        logging.info(f"{self.name} is preparing to rap against {opponent_name}.")
        chat_instance = Chat(prompt=f"{self.name} vs {opponent_name}: {prompt}")
        rap_line = chat_instance()
        logging.info(f"{self.name} delivered the following rap: {rap_line}")
        self.history.append(rap_line)
        return rap_line

    def judge(self, rap1: str, rap2: str, prompt: str) -> bool:
        logging.info(f"{self.name} is preparing to judge the following raps:\nRap 1: {rap1}\nRap 2: {rap2}")
        judgment_prompt = f"Judge the rap battle between two rappers:\nRap 1: {rap1}\nRap 2: {rap2}\n{prompt}"
        chat_instance = Chat(prompt=judgment_prompt)
        decision = bool_prompt(chat_instance)
        logging.info(f"{self.name} has made a decision: {'Rap 1 wins' if decision else 'Rap 2 wins'}")
        self.history.append(judgment_prompt)
        return decision

# Automated Profiling and Optimization decorator
def automated_profiling_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        analyze_performance(execution_time)
        return result
    return wrapper
