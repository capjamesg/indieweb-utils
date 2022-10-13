import pytest


@pytest.fixture
def article() -> str:
    with open("tests/fixtures/article.html") as f:
        return f.read()


@pytest.fixture
def post() -> str:
    with open("tests/fixtures/post.html") as f:
        return f.read()


@pytest.fixture
def article_url() -> str:
    return "https://jamesg.blog/2021/12/06/advent-of-bloggers-6/"


@pytest.fixture
def index() -> str:
    with open("tests/fixtures/index.html") as f:
        return f.read()


@pytest.fixture
def index2() -> str:
    with open("tests/fixtures/index2.html") as f:
        return f.read()


@pytest.fixture
def in_reply_to() -> str:
    with open("tests/fixtures/in_reply_to.html") as f:
        return f.read()


@pytest.fixture
def reply1() -> str:
    with open("tests/fixtures/reply1.html") as f:
        return f.read()


@pytest.fixture
def reply2() -> str:
    with open("tests/fixtures/reply2.html") as f:
        return f.read()


@pytest.fixture
def reply3() -> str:
    with open("tests/fixtures/reply3.html") as f:
        return f.read()


@pytest.fixture
def reply4() -> str:
    with open("tests/fixtures/reply4.html") as f:
        return f.read()


@pytest.fixture
def reply5() -> str:
    with open("tests/fixtures/reply5.html") as f:
        return f.read()


@pytest.fixture
def reply6() -> str:
    with open("tests/fixtures/reply6.html") as f:
        return f.read()


@pytest.fixture
def author2() -> str:
    with open("tests/fixtures/author2.html") as f:
        return f.read()


@pytest.fixture
def representative_index() -> str:
    with open("tests/fixtures/representative_page.html") as f:
        return f.read()


@pytest.fixture
def index_url() -> str:
    return "https://jamesg.blog/"
