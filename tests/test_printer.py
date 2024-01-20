import pytest

from selfdocprint import DictLayout, InlineLayout, MinimalLayout, ScrollLayout
from selfdocprint._printer import _get_edges, _Pane, _strip_styles, press
from tests.global_test_values import (
    _dict,
    _list,
    _set,
    _tuple,
    bf,
    bt,
    f,
    f_expr,
    formula,
    i,
    i_expr,
    layouts_expected_output,
    s,
    s_expr,
    theta,
    x,
)


class Test_press_with_all_layouts:
    # inline
    def test_press_of_inline_layout_integer(self, capsys):
        assert _strip_styles(press([i_expr], [i], InlineLayout)) == "\ni: -99"

    def test_press_of_inline_layout_string(self, capsys):
        assert (
            _strip_styles(press([s_expr], [s], InlineLayout))
            == "\ns: tic    \n   tacable\n   toes   "
        )

    def test_press_of_inline_layout_integer_and_string(self, capsys):
        assert (
            _strip_styles(press([i_expr, s_expr], [i, s], InlineLayout))
            == "\ni: -99  s: tic    \n           tacable\n           toes   "
        )


class Test_Pane_with_all_Layouts_and_types:
    # inline
    def test_pane_of_inline_layout_integer(self, capsys):
        assert _strip_styles(str(_Pane(InlineLayout, "i", i, 20))) == "i: -99"

    def test_pane_of_inline_layout_float(self, capsys):
        assert _strip_styles(str(_Pane(InlineLayout, "f", f, 20))) == "f: 99.555555"

    def test_pane_of_inline_layout_string(self, capsys):
        assert (
            _strip_styles(str(_Pane(InlineLayout, "s", s, 20)))
            == "s: tic    \n   tacable\n   toes   "
        )


class Test_get_edges:
    def test_get_edges_empty(self):
        assert _get_edges("", "") == ("", "", "", "")

    def test_get_edges_no_line_feeds(self):
        assert _get_edges("|-", "-|") == ("", "|-", "-|", "")

    def test_get_edges_with_line_feeds(self):
        assert _get_edges("\n|-", "-|\n") == ("\n", "|-", "-|", "\n")

    def test_get_edges_line_feeds_only(self):
        assert _get_edges("\n\n", "\n\n") == ("\n\n", "", "", "\n\n")
