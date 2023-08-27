import ast

# constant test values that are used in many tests declared globally
# probably not the best way but can't figure out how to do it in a better way
bf = False
bt = True
i = -99
f = 99.555555
s = "tic\ntacable\ntoes"
formula = "The Ultimate Question of Life,\nthe Universe, and Everything"
theta = 6.006
x = 7
_list = [1, 2, 3, 4]
_tuple = (1, 2, 3, 4)
_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
_set = {"a", "b", "c", "d"}

i_expr = ast.parse('i').body[0].value
f_expr = ast.parse('f').body[0].value
s_expr = ast.parse('s').body[0].value

sty = "\x1B[95m"
sto = "\x1B[0m"

layouts_expected_output = {  # expected results for the different layout test
    "inline": {
        "integer": f"\n{sty}i: {sto}     -99\n",
        "float": f"\n{sty}f: {sto}      99.556\n",
        "string": f"\n{sty}s: {sto}tic    \n   tacable\n   toes   \n",
        "expression": f"\n{sty}i * f: {sto}   -9856.000\n",
        "all_values": f"\n{sty}i: {sto}     -99   {sty}f: {sto}      99.556   {sty}s: {sto}tic    \n                                   tacable\n                                   toes   \n",
    },
    "dict": {
        "integer": f"\n{sty}i : {sto}     -99\n",
        "float": f"\n{sty}f : {sto}      99.556\n",
        "string": f"\n{sty}s : {sto}tic    \n    tacable\n    toes   \n",
        "expression": f"\n{sty}i * f : {sto}   -9856.000\n",
        "all_values": f"\n{sty}i : {sto}     -99\n{sty}f : {sto}      99.556\n{sty}s : {sto}tic    \n    tacable\n    toes   \n",
    },
    "scroll": {
        "integer": f"\n{sty}i:\n{sto}-99\n\n",
        "float": f"\n{sty}f:\n{sto}99.555555\n\n",
        "string": f"\n{sty}s:\n{sto}tic\ntacable\ntoes\n\n",
        "expression": f"\n{sty}i * f:\n{sto}-9855.999945\n\n",
        "all_values": f"\n{sty}i:\n{sto}-99\n\n{sty}f:\n{sto}99.555555\n\n{sty}s:\n{sto}tic\ntacable\ntoes\n\n",
    },
    "minimal": {
        "integer": f"{sty}i:{sto}-99\n",
        "float": f"{sty}f:{sto}99.555555\n",
        "string": f"{sty}s:{sto}tic\ntacable\ntoes\n",
        "expression": f"{sty}i * f:{sto}-9855.999945\n",
        "all_values": f"{sty}i:{sto}-99 {sty}f:{sto}99.555555 {sty}s:{sto}tic\ntacable\ntoes\n",
    },
}
