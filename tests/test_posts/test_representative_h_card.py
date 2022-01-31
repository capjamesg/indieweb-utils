import pytest


class TestRepresentativeHCard:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_representative_h_card

        return get_representative_h_card

    def test_representative_h_card(self, target):
        url = "https://aaronparecki.com"

        assert target(url) != {}
