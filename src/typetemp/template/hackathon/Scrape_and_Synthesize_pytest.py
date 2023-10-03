from pytest_bdd import given, when, then, parsers, scenarios

scenarios("Scrape_and_Synthesize.feature")


@given("a valid URL")
def given_function():
    pass


@when("the scraper runs")
def when_function():
    pass


@then("the data should be saved locally")
def then_function():
    pass


@given("raw data")
def given_function():
    pass


@when("data cleaning is done")
def when_function():
    pass


@then("a clean dataset should be created")
def then_function():
    pass


@given("a dataset")
def given_function():
    pass


@when("an analysis is performed")
def when_function():
    pass


@then("summaries and plans should be generated")
def then_function():
    pass
