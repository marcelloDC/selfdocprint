import subprocess


def ipynb_to_markdown():
    cp = subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "readme.ipynb",
            "--to",
            "markdown",
        ]
    )
    print(cp.returncode)
    return


def add_image_references():
    with open("readme.md") as f:
        source = f.readlines()

    i = iter(source)
    image_count = 0
    with open("readme.md", "w") as f:
        while (l := next(i, None)) is not None:
            f.write(l)
            if l == "```\n":
                f.write(
                    next(i)
                )  # read the empty line after triple backtick code block closing
                image_count += 1
                f.write(
                    f"![image {image_count}](./images/output_image_{image_count}.png)\n\n"
                )


def main():
    """A script to convert readme.ipynb to readme.md and add
    image references for output images in readme.md."""

    ipynb_to_markdown()
    add_image_references()


if __name__ == "__main__":
    main()
