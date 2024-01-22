import pytest

import selfdocprint as sdp
from selfdocprint import (
    AutoLayout,
    DictLayout,
    InlineLayout,
    MinimalLayout,
    PrintFunc,
    ScrollLayout,
    TableLayout,
)
from selfdocprint._printer import _strip_styles
from selfdocprint.selfdocprint import _context_warning
from selfdocprint.selfdocprint import _print as print
from tests.global_test_values import (
    _dict,
    _list,
    _set,
    _tuple,
    bf,
    bt,
    f,
    formula,
    i,
    layouts_expected_output,
    s,
    s_12_lines,
    theta,
    x,
)


class TestLayouts:
    # auto
    def test_auto_layout_new_row(self, capsys):
        print(formula, theta, x, theta * x, 1/3, 1/6, 1/9)
        assert (
            _strip_styles(capsys.readouterr().out)
            == layouts_expected_output["auto"]["row_too_long"]
        )

    def test_auto_layout_too_high_value(self, capsys):
        print(formula, theta, x, theta * x, s_12_lines, 1/3, 1/6, 1/9)
        assert (
            _strip_styles(capsys.readouterr().out)
            == layouts_expected_output["auto"]["value_too_high"]
        )

    # inline
    def test_inline_layout_integer(self, capsys):
        print(i, layout=InlineLayout())
        assert capsys.readouterr().out == layouts_expected_output["inline"]["integer"]

    def test_inline_layout_float(self, capsys):
        print(f, layout=InlineLayout())
        assert capsys.readouterr().out == layouts_expected_output["inline"]["float"]

    def test_inline_layout_string(self, capsys):
        print(s, layout=InlineLayout())
        assert capsys.readouterr().out == layouts_expected_output["inline"]["string"]

    def test_inline_layout_expression(self, capsys):
        print(i * f, layout=InlineLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["inline"]["expression"]
        )

    def test_inline_layout_all_values(self, capsys):
        print(i, f, s, layout=InlineLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["inline"]["all_values"]
        )

    # dict
    def test_dict_layout_integer(self, capsys):
        print(i, layout=DictLayout())
        assert capsys.readouterr().out == layouts_expected_output["dict"]["integer"]

    def test_dict_layout_float(self, capsys):
        print(f, layout=DictLayout())
        assert capsys.readouterr().out == layouts_expected_output["dict"]["float"]

    def test_dict_layout_string(self, capsys):
        print(s, layout=DictLayout())
        assert capsys.readouterr().out == layouts_expected_output["dict"]["string"]

    def test_dict_layout_expression(self, capsys):
        print(i * f, layout=DictLayout())
        assert capsys.readouterr().out == layouts_expected_output["dict"]["expression"]

    def test_dict_layout_all_values(self, capsys):
        print(i, f, s, layout=DictLayout())
        assert capsys.readouterr().out == layouts_expected_output["dict"]["all_values"]

    # scroll
    def test_scroll_layout_integer(self, capsys):
        print(i, layout=ScrollLayout())
        assert capsys.readouterr().out == layouts_expected_output["scroll"]["integer"]

    def test_scroll_layout_float(self, capsys):
        print(f, layout=ScrollLayout())
        assert capsys.readouterr().out == layouts_expected_output["scroll"]["float"]

    def test_scroll_layout_string(self, capsys):
        print(s, layout=ScrollLayout())
        assert capsys.readouterr().out == layouts_expected_output["scroll"]["string"]

    def test_scroll_layout_expression(self, capsys):
        print(i * f, layout=ScrollLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["scroll"]["expression"]
        )

    def test_scroll_layout_all_values(self, capsys):
        print(i, f, s, layout=ScrollLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["scroll"]["all_values"]
        )

    # minimal
    def test_minimal_layout_integer(self, capsys):
        print(i, layout=MinimalLayout())
        assert capsys.readouterr().out == layouts_expected_output["minimal"]["integer"]

    def test_minimal_layout_float(self, capsys):
        print(f, layout=MinimalLayout())
        assert capsys.readouterr().out == layouts_expected_output["minimal"]["float"]

    def test_minimal_layout_string(self, capsys):
        print(s, layout=MinimalLayout())
        assert capsys.readouterr().out == layouts_expected_output["minimal"]["string"]

    def test_minimal_layout_expression(self, capsys):
        print(i * f, layout=MinimalLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["minimal"]["expression"]
        )

    def test_minimal_layout_all_values(self, capsys):
        print(i, f, s, layout=MinimalLayout())
        assert (
            capsys.readouterr().out == layouts_expected_output["minimal"]["all_values"]
        )

    # table
    def test_table_layout(self, capsys):
        for i in range(5):
            print(i, i**2, 1 / 0.01, i * 2, layout=sdp.TableLayout)
        assert (
            _strip_styles(capsys.readouterr().out) == layouts_expected_output["table"]["normal"]
        )

    def test_table_layout_widened_columns(self, capsys):
        for i in range(5):
            print(i, i**2, 1 / (i + 0.000001), i * 2, layout=sdp.TableLayout)
        assert (
            _strip_styles(capsys.readouterr().out) == layouts_expected_output["table"]["widened_columns"]
        )


class TestEdgeCases:
    def test_single_value_str_literal_prints_without_label(self, capsys):
        print("test", layout=MinimalLayout())
        assert capsys.readouterr().out == "test\n"

    def test_single_value_int_literal_prints_without_label(self, capsys):
        print(1, layout=MinimalLayout())
        assert capsys.readouterr().out == "1\n"

    def test_single_value_fstring_literal_prints_without_label(self, capsys):
        print(f"test{i}", layout=MinimalLayout())
        assert capsys.readouterr().out == "test-99\n"


class TestContextWarning:
    def test_context_warning_and_that_it_is_displayed_only_once(self, capsys):
        eval("print(i, layout=MinimalLayout)")
        eval("print(i, layout=MinimalLayout)")
        assert capsys.readouterr().out == f"{_context_warning}\n-99\n-99\n"


class TestCreateCustomPrintFunction:
    def test_with_inline_as_default_layout(self, capsys):
        prinline = PrintFunc(default_layout=InlineLayout)
        prinline(i)
        assert capsys.readouterr().out == layouts_expected_output["inline"]["integer"]

    def test_override_layout_to_none_in_call(self, capsys):
        prinline = PrintFunc(default_layout=InlineLayout)
        prinline(i, f, layout=None)
        assert capsys.readouterr().out == "-99 99.555555\n"


class TestPrintSpec:
    def test_print_specs_does_not_crash(self, capsys):
        sdp.print_layout_specs()
