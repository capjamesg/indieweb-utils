def test_import_scope_constant():
    """Check that importing SCOPE_DEFINITIONS does not raise an error."""

    from indieweb_utils import SCOPE_DEFINITIONS

    assert SCOPE_DEFINITIONS != {}
