import responses
from indieweb_utils.indieauth import happ


@responses.activate
def test_handles_missing_name():
    """Test name is set to the me url if no name found."""
    web_page = """
    <div class='h-app'>
        <h1><a href="https://example.com" class="u-url p-name">Application Name</a></h1>
        <p class="p-summary">Application Summary</p>
        <img src="https://example.com/me.jpg" class="u-photo u-logo"/>
    </div>
    """

    response = happ.get_h_app_item(web_page)
    assert response.name == "Application Name"
    assert response.url == "https://example.com"
    assert response.logo == "https://example.com/me.jpg"
    assert response.summary == "Application Summary"
