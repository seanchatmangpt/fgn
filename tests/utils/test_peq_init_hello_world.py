import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from utils.peq import Peq

scenarios("peq_init_hello_world.feature")


@given(parsers.parse("there is a {filename} with content {content}"))
def create_module_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


@when(parsers.parse("I initialize Peq with filepath {filename}"))
def init(peq, filename):
    peq[0] = Peq(filepath=filename)


@then("the module should be loaded into Peq")
def module_loaded(peq):
    assert peq[0].module is not None


@then(parsers.parse("I should be able to access the {function_name} function"))
def access_function(peq, function_name):
    assert hasattr(peq[0].module, function_name)


@then(parsers.parse('the {function_name} function should return "{expected_output}"'))
def call_and_check_function(peq, function_name, expected_output):
    func = getattr(peq[0].module, function_name)
    assert func() == expected_output
