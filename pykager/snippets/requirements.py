from pathlib import Path
from typing import Optional

from ..snippets.snippet import Snippet
from ..utils import cached_property


class Requirements(Snippet):

    def __init__(self, directory: Path):
        super().__init__("requirements")
        self.__directory = directory

    def __repr__(self):
        return f"<Requirements requirements_file={self.requirements_file!r}>"

    @property
    def directory(self):
        return self.__directory

    @cached_property
    def requirements_file(self) -> Optional[Path]:
        if self.is_file:
            return Path("requirements.txt")

    @cached_property
    def is_file(self):
        return (self.directory / "requirements.txt").is_file()

    @property
    def code(self):
        return f"with open('{self.requirements_file}', 'r') as req_file:\n" \
               f"    requirements = [x for x in req_file.read().splitlines() if x and not x.startswith('#')]\n"

    @property
    def write_code(self) -> bool:
        return self.is_file
