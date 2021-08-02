from argparse import ArgumentParser
from pathlib import Path

from pykager.lib import Git, Setup, Readme
from pykager.snippets import Snippet
from pykager.utils import cached_property


class Pykager(ArgumentParser):
    __slots__ = (
        "name",
        "version",
        "author",
        "author_email",
        "url",
        "license",
        "description",
        "long_description",
        "keywords",
        "platforms",
        "classifiers",
        "download_url",
        "install_requires",
        "python_requires",
        "zip_safe",
        "packages",
        "entry_points",
    )

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", help="input directory (default: cwd)")
        self.name = self.setup_py.name or self.git.name
        self.version = self.setup_py.version
        self.author = self.setup_py.author or self.git.author.name
        self.author_email = self.setup_py.author_email or self.git.author.email
        self.url = self.setup_py.url or self.git.url
        self.license = self.setup_py.license
        self.description = self.setup_py.description
        self.long_description = None
        self.keywords = self.setup_py.keywords
        self.platforms = self.setup_py.platforms
        self.classifiers = self.setup_py.classifiers
        self.download_url = self.setup_py.download_url
        self.install_requires = None
        self.python_requires = self.setup_py.python_requires
        self.zip_safe = self.setup_py.zip_safe
        self.packages = self.setup_py.packages
        self.entry_points = self.setup_py.entry_points

    @cached_property
    def git(self):
        return Git(self.input_dir)

    @cached_property
    def setup_py(self):
        return Setup(self.input_dir)

    @cached_property
    def readme(self):
        return Readme(self.input_dir)

    @cached_property
    def args(self):
        return self.parse_args()

    @cached_property
    def input_dir(self):
        if self.args.input:
            input_dir = Path(self.args.input).resolve()
        elif __name__ == "__main__":
            input_dir = Path.cwd().parent
        else:
            input_dir = Path.cwd()

        if not input_dir.is_dir():
            input_dir = input_dir.parent
        return input_dir

    @property
    def code(self) -> str:
        code = "from setuptools import setup\n" \
               "\n"

        arg_dict = {arg: getattr(self, arg) for arg in self.__slots__}

        for arg, value in arg_dict.items():
            if isinstance(value, Snippet):
                code += value.code
                code += "\n"

        code += "\n" \
                "setup(\n"

        for arg, value in arg_dict.items():
            if isinstance(value, Snippet):
                value = value.variable
            if value is not None:
                code += f"    {arg}={value},\n"
        return code + ")"


if __name__ == "__main__":
    p = Pykager()
    print(p.code)
