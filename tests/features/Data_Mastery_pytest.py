from pytest_bdd import given, when, then, parsers, scenarios

scenarios("Data Mastery.feature")


@given("missing data")
def given_function():
    pass


@when("the imputation algorithm runs")
def when_function():
    pass


@then("the dataset should be complete")
def then_function():
    pass


@given("unlabelled data")
def given_function():
    pass


@when("a labeling algorithm runs")
def when_function():
    pass


@then("the dataset should be labelled")
def then_function():
    pass


@given("unordered data")
def given_function():
    pass


@when("the sorting algorithm runs")
def when_function():
    pass


@then("the data should be sorted")
def then_function():
    pass
