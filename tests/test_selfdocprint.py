import pytest
from tests.global_test_values import (
    bf,
    bt,
    i,
    f,
    s,
    formula,
    theta,
    x,
    _list,
    _tuple,
    _dict,
    _set,
    layouts_expected_output,
)

import selfdocprint as sdp
from selfdocprint import PrintFunc
from selfdocprint import InlineLayout, DictLayout, ScrollLayout, MinimalLayout

print = PrintFunc()


class TestLayouts:
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


class TestConfiguringDefaultLayout:
    def test_configure_to_inline(self, capsys):
        prinline = PrintFunc(default_layout=InlineLayout)
        prinline(i)
        assert capsys.readouterr().out == layouts_expected_output["inline"]["integer"]

    def test_configured_to_inline_and_reset_to_none_in_call(self, capsys):
        prinline = PrintFunc(default_layout=InlineLayout)
        prinline(i, f, layout=None)
        assert capsys.readouterr().out == "-99 99.555555\n"


class TestPrintSpec:
    def test_print_specs_does_not_crash(self, capsys):
        sdp.print_layout_specs()
