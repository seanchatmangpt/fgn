from urllib.parse import urljoin

import pytest
from pytest_bdd import scenario, given, when, then


class Author:
    def __init__(self):
        self.user = None


class Auth:
    def __init__(self):
        self.user = None


class Article:
    def __init__(self, id, is_published):
        self.id = id
        self.is_published = is_published

    def refresh(self):
        pass


class Browser:
    def visit(self, url):
        pass

    def find_by_css(self, selector):
        pass

    @property
    def url(self):
        return "http://localhost:5000"


@pytest.fixture
def auth():
    return Auth()


@pytest.fixture
def author():
    return Author()


@scenario("publish_article.feature", "Publishing the article")
def test_publish():
    pass


@pytest.fixture
def browser():
    return Browser()


@given("I'm an author user")
def author_user(auth, author):
    auth.user = author.user


def create_test_article(author):
    return Article(id=1, is_published=False)


@given("I have an article", target_fixture="article")
def article(author):
    return create_test_article(author=author)


@when("I go to the article page")
def go_to_article(article, browser):
    browser.visit(urljoin(browser.url, "/manage/articles/{0}/".format(article.id)))


@when("I press the publish button")
def publish_article(browser):
    browser.find_by_css("button[name=publish]").first.click()


class ElementDoesNotExist:
    pass


@then("I should not see the error message")
def no_error_message(browser):
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".message.error").first


@then("the article should be published")
def article_is_published(article):
    article.refresh()  # Refresh the object in the SQLAlchemy session
    assert article.is_published
