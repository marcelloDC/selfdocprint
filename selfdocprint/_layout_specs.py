from dataclasses import dataclass

DEFAULT_STYLE: str = "95"


@dataclass
class Layout:
    """Defines a layout"""

    lbl_format: str = ""
    int_format: str = ""
    float_format: str = ""
    str_format: str = ""
    style: str = DEFAULT_STYLE
    pointer: str = ""
    literal_lbl: str = ""
    head: str = ""
    tail: str = ""
    seperator: str = ""
    alt_layout: "Layout" = None
    max_width: int = None
    max_height: int = None


@dataclass
class DefaultLayout(Layout):
    """Only used in the function declaration to indicate that by default
    the `layout` kwarg is set to self.default_layout."""


@dataclass
class MinimalLayout(Layout):
    """Prints a label in front of each value."""

    seperator: str = " "
    pointer: str = ":"


@dataclass
class InlineLayout(Layout):
    """Prints a label in front of its value.
    Label/value pairs are printed from left to right.
    Multi-line value strings are properly aligned."""

    str_format: str = "<{value_width}"
    seperator: str = "  "
    pointer: str = ": "


@dataclass
class DictLayout(Layout):
    """Prints a label in front of its value.
    Label/value pairs are printed from top to bottom.
    Multi-line value strings are properly aligned."""

    lbl_format: str = "<{max_label_width}"
    int_format: str = "-8"
    float_format: str = "-12.3f"
    str_format: str = "<{value_width}"
    seperator: str = "\n"
    pointer: str = " : "
    literal_lbl: str = "_"


@dataclass
class ScrollLayout(Layout):
    """Prints a label above its value.
    Label/value pairs are printed from top to bottom."""

    seperator: str = "\n"
    pointer: str = ":\n"


@dataclass
class AutoLayout(Layout):
    """Uses InlineLayout with the following additions: 1) if the next label/value pair would exceed
    max_width then a new row is started, 2) if a label/value pair exceeds max_height then it is printed
    using alt_layout."""

    str_format: str = "<{value_width}"
    seperator: str = "  "
    pointer: str = ": "
    alt_layout: Layout = ScrollLayout
    max_width: int = 140
    max_height: int = 10


@dataclass
class TableLayout(Layout):
    """Prints a label above its value.
    Label/value pairs are printed from left to right.
    Multi-line value strings are properly aligned."""

    # head: str = "\n"
    # tail: str = " |"
    seperator: str = " | "
    lbl_format: str = ">{value_width}"
    int_format: str = "-8"
    float_format: str = "-12.3f"
    str_format: str = "<{value_width}"
    pointer: str = "\n"
    literal_lbl: str = "_"
