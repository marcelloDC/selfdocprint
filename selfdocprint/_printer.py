import ast
import io
import re
from contextlib import closing
from typing import Callable

from ._layout_specs import Layout


class _Pane:
    """Holds a formatted and layed-out label/value pair."""

    def __init__(
        self,
        layout: Layout,
        label: str,
        value: object,
        max_label_width: int,
        include_label: bool = True,
    ):
        # format the value
        if value is None:
            value_lines = [""]
            value_width = 0
        elif isinstance(value, bool):
            value_lines = [str(value)]
            value_width = len(value_lines[0])
        elif isinstance(value, int):
            value_lines = [format(value, layout.int_format)]
            value_width = len(value_lines[0])
        elif isinstance(value, float):
            value_lines = [format(value, layout.float_format)]
            value_width = len(value_lines[0])
        else:
            value_lines = str(value).split("\n")
            value_width = max(len(vl) for vl in value_lines)
            # if not fixed the the width of the string value format spec can only be value_width
            format_spec = layout.str_format.replace("{value_width}", str(value_width))
            value_lines = [format(v, format_spec) for v in value_lines]

        if label == "":
            label_line = ""
        else:
            # format the label and apend the pointer
            ## if not fixed, the width in the label format spec can either be value_width or max_label_width
            format_spec = layout.lbl_format.replace("{value_width}", str(value_width))
            format_spec = format_spec.replace("{max_label_width}", str(max_label_width))
            label_line = format(label, format_spec) + layout.pointer

            last_new_line_ofs = label_line.rfind("\n")
            if last_new_line_ofs == -1:
                if _has_alignment(layout):
                    # indent the value lines
                    indent = " " * len(label_line)
                    value_lines = [
                        s if i == 0 else indent + s for i, s in enumerate(value_lines)
                    ]
                label_line = f"{sgr(layout.style)}{label_line}{sgr()}"
            else:
                # maybe TODO implement possible feature here: custom indents
                max_label_line_width = max(len(l) for l in label_line.split("\n"))
                if _has_alignment(layout) and max_label_line_width > value_width:
                    indent = " " * (max_label_line_width - value_width)
                    value_lines = [indent + l for l in value_lines]
                label_line = f"{sgr(layout.style)}{label_line[:last_new_line_ofs]}{sgr()}{label_line[last_new_line_ofs:]}"

        self.layout = layout
        if include_label:
            self.lines: list(str) = (label_line + "\n".join(value_lines)).split("\n")
        else:
            self.lines: list(str) = value_lines
        self.width: int = max(len(_strip_styles(l)) for l in self.lines)
        self.height: int = len(self.lines)

    def __str__(self):
        return "\n".join(self.lines)

    def get_line(self, i: int):
        if i < self.height:
            return self.lines[i]
        else:
            if _has_alignment(self.layout):
                return " " * self.width
            else:
                return ""


def press(
    args: list[ast.expr],
    values: list[object],
    layout: Layout,
    beg: str,
    end: str,
    press_labels: bool = True,
) -> str:
    labels = [_create_label(arg, layout.literal_lbl) for arg in args]
    max_lbl_width: int = _getlongest_line_len(labels)
    _beg, pre, post, _end = _get_edges(beg + layout.head, layout.tail + end)

    with closing(io.StringIO("")) as buf:
        if press_labels:
            buf.write(_beg)
        current_width = 0
        pane_row = []
        for i, (lbl, val) in enumerate(zip(labels, values, strict=True)):
            pane = _Pane(layout, lbl, val, max_lbl_width, press_labels)
            if _isleft_to_right_layout(layout) and _has_alignment(layout):
                if (layout.max_width is not None and pane.width > layout.max_width) or (
                    layout.max_height is not None and pane.height > layout.max_height
                ):
                    # the pane is too high or too wide, it has to be placed in its own row
                    if len(pane_row) > 0:
                        pane_row = _flush_pane_row(pane_row, buf, layout, pre, post)
                        buf.write("\n")
                    current_width = 0
                    alt_layout = layout.alt_layout()
                    alt_pane = _Pane(alt_layout, lbl, val, max_lbl_width, press_labels)
                    pane_row = _flush_pane_row([alt_pane], buf, alt_layout, pre, post)
                    buf.write("\n")
                elif (
                    layout.max_width is not None
                    and current_width + pane.width > layout.max_width
                ):
                    # with the new pane the horizontal pane sequence would become too long
                    pane_row = _flush_pane_row(pane_row, buf, layout, pre, post)
                    buf.write("\n")
                    current_width = pane.width
                    pane_row.append(pane)
                else:
                    current_width += pane.width
                    pane_row.append(pane)
            else:  # not _isleft_to_right_layout(layout) and _has_alignment(layout)
                if i > 0:
                    buf.write(layout.seperator)
                pane_row = _flush_pane_row([pane], buf, layout, pre, post)

        _flush_pane_row(pane_row, buf, layout, pre, post)
        buf.write(_end)
        return buf.getvalue()


def _flush_pane_row(pane_row, buf, layout, pre="", post=""):
    if len(pane_row) > 0:
        max_lines = max([pane.height for pane in pane_row])
        for l in range(max_lines):
            buf.write(pre)
            buf.write(layout.seperator.join(pane.get_line(l) for pane in pane_row))
            buf.write(post)
            if l < max_lines - 1:
                buf.write("\n")
    return []


def sgr(sgr_codes: str = None):
    if sgr_codes is None:
        sgr_codes = "0"
    return f"\033[{sgr_codes}m"


def _has_alignment(layout: Layout):
    return re.match(r".*[<>^].*", layout.str_format) is not None


def _isleft_to_right_layout(layout: Layout) -> bool:
    for attr in ["seperator"]:
        if "\n" in getattr(layout, attr):
            return False
    return True


def _get_edges(beg: str, end: str):
    if (last_nl := beg.rfind("\n")) != -1:
        pre = beg[last_nl + 1 :]
        beg = beg[: last_nl + 1]
    else:
        pre = beg
        beg = ""

    if (first_nl := end.find("\n")) != -1:
        post = end[:first_nl]
        end = end[first_nl:]
    else:
        post = end
        end = ""

    return beg, pre, post, end


# def _OLD_fixate_alignment_width(format_spec: str, fixed_width: int):
#     """Checks for an 'align' char in format_spec and appends fixed_width if the
#     width for the alignment is not specified"""

#     # The following pattern captures an align specification without a width: an align character,
#     # followed by zero or more '0' chars (specified inside an Atomic group), but not followed by a digit.
#     pattern = r"([<>^](?>0*))(?![1-9])"
#     return re.sub(
#         pattern,
#         r"\g<1>" + str(fixed_width),
#         format_spec,
#         count=1,
#     )


def _getlongest_line_len(strs: list[str]) -> int:
    """check each line in each string in strs and return the longest line"""
    longest_lines = [max(s.split("\n"), key=len) for s in strs]
    if len(longest_lines) == 0:
        return 0
    else:
        return len(max(longest_lines, key=len))


def _strip_styles(s: str) -> str:
    """returns s with style codes removed"""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    result = ansi_escape.sub("", s)
    return result


def _create_label(arg: ast.expr, literal_str: str):
    # for info on ast types: https://greentreesnakes.readthedocs.io/en/latest/nodes.html
    DEPRECATED_STR = f"Unexpected argument: {ast.unparse(arg)} (ast type is deprecated)"
    NOT_POSSIBLE_STR = f"Unexpected argument: {ast.unparse(arg)} (shouldn't be possible as arg in print() )"
    UNSUPPORTED = f"Unsupported argument: {ast.unparse(arg)}"
    # print(type(arg))
    for arg_type, action in [
        (ast.Attribute, ast.unparse),
        (ast.Await, UNSUPPORTED),
        (ast.BinOp, ast.unparse),
        (ast.BoolOp, ast.unparse),
        (ast.Bytes, DEPRECATED_STR),
        (ast.Call, ast.unparse),
        (ast.Compare, ast.unparse),
        (ast.Constant, lambda x: literal_str),
        (ast.Dict, lambda x: literal_str),
        (ast.DictComp, ast.unparse),
        (ast.Ellipsis, DEPRECATED_STR),
        (ast.FormattedValue, NOT_POSSIBLE_STR),
        (ast.GeneratorExp, ast.unparse),
        (ast.IfExp, ast.unparse),
        (ast.JoinedStr, lambda x: literal_str),
        (ast.Lambda, ast.unparse),
        (ast.List, lambda x: literal_str),
        (ast.ListComp, ast.unparse),
        (ast.Name, ast.unparse),
        (ast.NameConstant, DEPRECATED_STR),
        (ast.NamedExpr, ast.unparse),
        (ast.Num, DEPRECATED_STR),
        (ast.Set, lambda x: literal_str),
        (ast.SetComp, ast.unparse),
        (ast.Slice, NOT_POSSIBLE_STR),
        (ast.Starred, UNSUPPORTED),
        (ast.Str, DEPRECATED_STR),
        (ast.Subscript, ast.unparse),
        (ast.Tuple, lambda x: literal_str),
        (ast.UnaryOp, ast.unparse),
        (ast.Yield, UNSUPPORTED),
        (ast.YieldFrom, UNSUPPORTED),
    ]:
        if isinstance(arg, arg_type):
            if isinstance(action, Callable):
                return action(arg)
            else:
                raise ValueError(action)
    return f"unknow arg encountered: {arg}"
