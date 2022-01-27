import mf2py
import pytest


class TestPostTypeDiscovery:
    @pytest.fixture
    def target(self):
        from indieweb_utils import get_post_type

        return get_post_type

    def test_post_type_discovery(self, target, article):
        parsed = mf2py.parse(doc=article)
        h_entry = [item for item in parsed["items"] if item.get("type") == ["h-entry"]]
        assert target(h_entry[0]) == "article"
