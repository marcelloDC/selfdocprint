import pytest
from tests.global_test_values import (
    bf,
    bt,
    i,
    f,
    s,
    i_expr,
    f_expr,
    s_expr,
    formula,
    theta,
    x,
    _list,
    _tuple,
    _dict,
    _set,
    layouts_expected_output,
)

from selfdocprint._printer import press, _Pane, _strip_styles
from selfdocprint import InlineLayout, DictLayout, ScrollLayout, MinimalLayout


class Test_press_with_all_layouts:
    # inline
    def test_press_of_inline_layout_integer(self, capsys):
        assert _strip_styles(press([i_expr], [i], InlineLayout)) == "\ni:      -99"

    def test_press_of_inline_layout_string(self, capsys):
        assert (
            _strip_styles(press([s_expr], [s], InlineLayout))
            == "\ns: tic    \n   tacable\n   toes   "
        )

    def test_press_of_inline_layout_integer_and_string(self, capsys):
        assert (
            _strip_styles(press([i_expr, s_expr], [i, s], InlineLayout))
            == "\ni:      -99   s: tic    \n                 tacable\n                 toes   "
        )


class Test_Pane_with_all_Layouts_and_types:
    # inline
    def test_pane_of_inline_layout_integer(self, capsys):
        assert _strip_styles(str(_Pane(InlineLayout, "i", i, 20))) == "i:      -99"

    def test_pane_of_inline_layout_float(self, capsys):
        assert _strip_styles(str(_Pane(InlineLayout, "f", f, 20))) == "f:       99.556"

    def test_pane_of_inline_layout_string(self, capsys):
        assert (
            _strip_styles(str(_Pane(InlineLayout, "s", s, 20)))
            == "s: tic    \n   tacable\n   toes   "
        )
