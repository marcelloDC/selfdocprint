# from selfdocprint import print
import selfdocprint as sdp
from selfdocprint import console, print

# global test variables
bf = False
bt = True
i = -99
f = 99.555555
s = "tic\ntacable\ntoes"
s_12_lines = "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten\neleven\ntwelve"

formula = "The Ultimate Question of Life,\nthe Universe, and Everything"
theta = 6.006
x = 7

_list = [1, 2, 3, 4]
_tuple = (1, 2, 3, 4)
_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
_set = {"a", "b", "c", "d"}


def auto_demo():
    print("\n*** AutoLayout examples ***\n")

    print("* normal row")
    print(formula, theta, x, "literal", x * theta)

    print("\n* row with break because the row is longer than 140 characters")
    print(formula, theta, x, "literal", x * theta, s, 1 / 3, 1 / 6, 1 / 9)

    print("\n* row with 2 breaks because the value: s_12_lines, has more than 10 lines")
    print(formula, theta, x, "literal", x * theta, s_12_lines, s, 1 / 3, 1 / 6, 1 / 9)


def inline_demo():
    print("\n\n*** InlineLayout examples ***\n")
    print(formula, theta, x, "literal", x * theta, layout=sdp.InlineLayout)


def scroll_demo():
    print(formula, theta, x, "literal", x * theta, layout=sdp.ScrollLayout)


def dict_demo():
    print(formula, theta, x, "literal", x * theta, layout=sdp.DictLayout)


def table_demo():
    for i in range(5):
        print(i, i**2, 1 / (i + 0.000001), i * 2, layout=sdp.TableLayout)


def main():
    console.clear(clear_buffer=True)
    auto_demo()
    inline_demo()
    # scroll_demo()
    # dict_demo()
    table_demo()


if __name__ == "__main__":
    main()
