import pytest
import responses


class TestRepresentativeHCard:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_representative_h_card

        return get_representative_h_card

    @responses.activate
    def test_representative_h_card(self, target, representative_index):
        """Test the representative h-card algorithm to find the representative h-card of a page."""
        url = "https://aaronparecki.com"

        responses.add(
            responses.Response(
                method="GET",
                url=url,
                body=representative_index,
            )
        )

        assert target(url) != {}
