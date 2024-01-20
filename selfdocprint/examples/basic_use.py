# from selfdocprint import print
import numpy as np

import selfdocprint as sdp
from selfdocprint import print

# from selfdocprint import DictLayout, InlineLayout, MinimalLayout, ScrollLayout, console, print
# from selfdocprint.selfdocprint import PrintFunc


# global test variables
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


def standard():
    arr = np.random.randint(100, size=(6, 5))
    # print(theta, x)
    print("test", formula, theta, x, "literal", theta * x, s, 1 / 3, 1 / 6, 1 / 9)
    print("test\ngedeyg", f"test: {x}")
    print("test\ngedeyg", f"test {x}", layout=None)


def table_demo():
    for i in range(10):
        print(i, i**2, 1 / (i + 0.000001), i*2, layout=sdp.TableLayout)


# def demo():
#     console.clear()
#     print("\n**************************************************")
#     print("***             Normal print output            ***")
#     print("**************************************************")
#     print()
#     print(formula, theta, x, theta * x)
#     print()
#     print()
#     print("**************************************************")
#     print("*** Self-documented and layed-out print output ***")
#     print("**************************************************")
#     print(
#         formula,
#         theta,
#         x,
#         theta * x,
#         beg="\n\n*** using inline layout ***\n",
#         layout=InlineLayout(),
#     )
#     print(
#         formula,
#         theta,
#         x,
#         theta * x,
#         beg="\n\n*** using dict layout ***\n",
#         layout=DictLayout(),
#     )
#     print(
#         formula,
#         theta,
#         x,
#         theta * x,
#         beg="\n\n*** using scroll layout ***\n",
#         layout=ScrollLayout(),
#     )
#     print(
#         formula,
#         theta,
#         x,
#         theta * x,
#         beg="\n*** using minimal layout ***\n\n",
#         layout=MinimalLayout(),
#         end="\n\n\n",
#     )
#     eval("print(x, layout=ScrollLayout)")
#     eval(
#         "print(x, layout=ScrollLayout)"
#          )


# def with_config():
#     print = PrintFunc(default_layout=MinimalLayout())
#     print(formula, theta, x, theta * x)


# def print_specs():
#     sdp.print_layout_specs()


def main():
    standard()
    table_demo()
    # demo()
    # with_config()
    # print_specs()


if __name__ == "__main__":
    main()
