import responses

from indieweb_utils.indieauth import happ


@responses.activate
def test_handles_missing_name():
    """Test name is set to the me url if no name found."""
    web_page = """
    <div class='h-app'>
        <h1 class="p-name">Application Name</h1>
        <p class="p-summary">Application Summary</p>
        <img src="https://example.com/me.jpg" class="u-photo u-logo"/>
    </div>
    """

    client_id = "https://example.com"
    redirect_uri = "https://example.com/authorize"

    response = happ.get_h_app_item(web_page, client_id, redirect_uri)
    assert response.name == "Application Name"
    assert response.url == "https://example.com"
    assert response.logo == "https://example.com/me.jpg"
    assert response.summary == "Application Summary"