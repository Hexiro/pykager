from pathlib import Path
from typing import Dict, Any

from ..utils import cached_property, safe_eval


class Setup:

    def __init__(self, directory: Path):
        self.__file = directory / "setup.py"

    @property
    def file(self):
        return self.__file

    def __getattr__(self, item):
        return self.kwargs.get(item)

    @cached_property
    def kwargs(self) -> Dict[str, Any]:
        if not self.file.is_file():
            return {}
        code = self.file.read_text(encoding="utf8", errors="ignore")
        code = code[code.find("setup("):]
        code = code[6:]
        code = code.lstrip().rstrip().rstrip(")").rstrip()
        # heal code
        kwargs = {}
        for line in code.splitlines():
            line = line.lstrip()
            keys = list(kwargs.keys())
            if "=" in line and line[0] not in ["'", "\""]:
                key, value = line.split("=", maxsplit=1)
                kwargs[key] = value
            elif keys:
                kwargs[keys[-1]] += line
        for key, value in kwargs.items():
            if value.endswith(","):
                value = value[:-1]
            if value is not None:
                kwargs[key] = safe_eval(value)
        return kwargs
