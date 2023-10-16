import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from utils.peq import Peq

scenarios("peq_dot_notation.feature")


@given(parsers.parse("there is a {filename} with content {content}"))
def create_module_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


@when(parsers.parse("I initialize Peq with filepath {filename}"))
def init(peq, filename):
    peq[0] = Peq(filepath=filename)


@then(parsers.parse("I should be able to add the function {function_name} using dot notation"))
def add_function_dot_notation(peq, function_name):
    def greet():
        return "Hello, World!"

    setattr(peq[0], function_name, greet)


@then(parsers.parse("calling {function_name} should return {expected_output}"))
def access_function_dot_notation(peq, function_name, expected_output):
    assert hasattr(peq[0].module, function_name)
    func = getattr(peq[0].module, function_name)
    assert func() == expected_output
