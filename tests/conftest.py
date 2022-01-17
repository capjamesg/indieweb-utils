import pytest


@pytest.fixture
def article() -> str:
    with open("tests/fixtures/article.html") as f:
        return f.read()


@pytest.fixture
def article_url() -> str:
    return "https://jamesg.blog/2021/12/06/advent-of-bloggers-6/"


@pytest.fixture
def index() -> str:
    with open("tests/fixtures/index.html") as f:
        return f.read()


@pytest.fixture
def index_url() -> str:
    return "https://jamesg.blog/"
