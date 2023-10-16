import os

import pytest
from pytest_bdd import given, scenarios, then, when, parsers

from utils.peq import Peq


scenarios("./Peq_-_Advanced_Python_Module_Management3.feature")


@given("there is no sample_module.py")
def given_function():
    if os.path.exists("sample_module.py"):
        os.remove("sample_module.py")


@when("I initialize Peq with filepath sample_module.py")
def when_function():
    global peq_instance
    peq_instance = Peq("sample_module.py")


@then("a new file sample_module.py should be created with content")
def then_function():
    assert os.path.exists("sample_module.py")
    with open("sample_module.py", "r") as f:
        content = f.read()
    assert content is not None


@then("the module should be loaded into Peq")
def then_function():
    """Check that the module is loaded into Peq.

    Implementation instructions:
    1. Check if the `peq_instance.module` attribute exists.
    2. Ensure that this module corresponds to the 'sample_module.py' file.
    """
    assert hasattr(peq_instance, "module")
    assert peq_instance.filepath == "sample_module.py"


@given(parsers.parse("there is a {filename} with content {content}"))
def setup_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)


@when(parsers.parse("I initialize Peq with filepath {filename}"))
@pytest.fixture
def initialize_peq(filename):
    return Peq(filename)


@then("the module should be loaded into Peq")
def check_module_loaded(initialize_peq):
    assert initialize_peq.module is not None


@then(parsers.parse("I should be able to access the {function_name} function"))
def access_function(initialize_peq, function_name):
    assert hasattr(initialize_peq.module, function_name)


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@when("I add a function greet with content 'def greet(): return Hello, World!'")
def when_function():
    pass


@then("the module should contain the greet function")
def then_function():
    pass


@then("calling greet should return Hello, World!")
def then_function():
    pass


@given("Peq is initialized with sample_module.py containing a function greet")
def given_function():
    pass


@when("I set the function greet to 'def greet(): return Goodbye, World!'")
def when_function():
    pass


@then("calling greet should return Goodbye, World!")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@given("I have added a function greet")
def given_function():
    pass


@when("I call the undo method")
def when_function():
    pass


@then("the function greet should no longer exist in the module")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@given("I have added a function greet")
def given_function():
    pass


@given("I have undone the change")
def given_function():
    pass


@when("I call the redo method")
def when_function():
    pass


@then("the function greet should exist in the module")
def then_function():
    pass


@given("Peq is initialized with sample_module.py with git integration enabled")
def given_function():
    pass


@given("there are multiple commits in the git history")
def given_function():
    pass


@when("I call the rollback method with steps 2")
def when_function():
    pass


@then("the sample_module.py should revert to its state from 2 commits ago")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@given("there are associated tests for the module")
def given_function():
    pass


@when("I call the test method")
def when_function():
    pass


@then("the tests should be executed")
def then_function():
    pass


@then("I should receive feedback on their pass/fail status")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@when(
    "I add an async function fetch_data with content 'async def fetch_data(): return Data fetched'"
)
def when_function():
    pass


@then("the module should contain the async function fetch_data")
def then_function():
    pass


@then("calling fetch_data asynchronously should return Data fetched")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@when("I add a dictionary DATA with the content '{ key: value }'")
def when_function():
    pass


@then("the module should contain the dictionary DATA")
def then_function():
    pass


@then("accessing DATA[key] should return value")
def then_function():
    pass


@given("Peq is initialized with sample_module.py containing a dictionary DATA")
def given_function():
    pass


@when("I set the dictionary DATA to '{ new_key: new_value }'")
def when_function():
    pass


@then("accessing DATA[new_key] should return new_value")
def then_function():
    pass


@then("DATA should not have a key key")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@when("I add an import import os")
def when_function():
    pass


@then("the module should contain the import for os")
def then_function():
    pass


@then("I should be able to use the os library functionalities")
def then_function():
    pass


@given("Peq is initialized with sample_module.py containing an import for os")
def given_function():
    pass


@when("I add another import for os")
def when_function():
    pass


@then("the module should still only have one import statement for os")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@when("I add a function using datetime without manually importing it")
def when_function():
    pass


@then("Peq should automatically import the datetime library")
def then_function():
    pass


@then("the module should contain the import for datetime")
def then_function():
    pass


@given("Peq is initialized with sample_module.py")
def given_function():
    pass


@given("I have added an import from functools import lru_cache")
def given_function():
    pass


@when("I add a decorated function cached_func with content @lru_cache")
def when_function():
    pass


@then("the module should contain the decorated function cached_func")
def then_function():
    pass


@then("calling cached_func should return 42")
def then_function():
    pass
