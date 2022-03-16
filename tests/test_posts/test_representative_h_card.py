import pytest
import responses


class TestRepresentativeHCard:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_representative_h_card

        return get_representative_h_card

    def test_representative_h_card(self, target, representative_index):
        url = "https://aaronparecki.com"

        responses.add(
            responses.Response(
                method="GET",
                url=url,
                body=representative_index,
            )
        )

        assert target(url) != {}
