from selfdocprint._printer import _strip_styles


class TestHelperFunctions:
    def test_strip_styles(self):
        assert _strip_styles("\x1b[96;3mi: \x1b[0m") == "i: "
