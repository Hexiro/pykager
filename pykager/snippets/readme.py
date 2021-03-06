from pathlib import Path
from typing import Optional

from ..snippets.snippet import Snippet
from ..utils import cached_property


class Readme(Snippet):
    readme_extensions = {
        # as according to https://github.com/github/markup/tree/master#markups
        # and https://packaging.python.org/guides/making-a-pypi-friendly-readme/#creating-a-readme-file
        # Markdown
        ".markdown": "text/markdown",
        ".mdown": "text/markdown",
        ".mkdn": "text/markdown",
        ".md": "text/markdown",
        # Plain Text
        ".txt": "text/plain",
        "": "text/plain",
        # reStructuredText
        ".rst": "text/x-rst"
    }

    def __init__(self, directory: Path):
        super().__init__("readme")
        self.__directory = directory

    @cached_property
    def readme_file(self) -> Optional[Path]:
        """
        Finds readme files in the specified directory
        README is case insensitive afaik
        """
        for f in self.directory.glob("*"):
            if f.name.upper().startswith("README") and f.suffix in self.readme_extensions:
                return f.relative_to(self.directory)

    @cached_property
    def is_file(self):
        return self.readme_file and (self.directory / self.readme_file).is_file()

    @cached_property
    def content_type(self) -> Optional[str]:
        if self.readme_file:
            return self.readme_extensions[self.readme_file.suffix]

    @property
    def directory(self):
        return self.__directory

    @property
    def code(self):
        return f"with open('{self.readme_file}', encoding='utf-8') as readme_file:\n" \
               "    readme = readme_file.read()\n"

    @property
    def write_code(self) -> bool:
        return self.is_file
