import logging
from pathlib import Path
from typing import List


from components.helpers import get_container, get_resource, classname

from components.core.target_template import TargetTemplate, FromStringTargetTemplate
from components.nlp.prefixes_engine import PrefixesEngine


class PrefixesTarget:
    PREFIXES_TARGET = """{% for pp in prefixes %} {{pp}}
    {% endfor %}
    """

    PREFIXES_TARGET_SUFFIX = ".md"

    def __init__(self, home: Path) -> None:
        self._home = home
        self._target_template: TargetTemplate = FromStringTargetTemplate(
            PrefixesTarget.PREFIXES_TARGET, suffix=PrefixesTarget.PREFIXES_TARGET_SUFFIX
        )

    @property
    def home(self) -> Path:
        return self._home

    @property
    def target_template(self) -> TargetTemplate:
        return self._target_template

    def save_prefixes(self, name: str, prefixes: List[str]) -> None:
        content = self.target_template.template.render(prefixes=prefixes)
        target_container = get_container(self.home, "prefixes")
        prefixes_file = get_resource(
            target_container, name, self.target_template.suffix
        )
        with open(prefixes_file, "w") as target:
            target.write(content)

    def execute(self, origin_resource: Path, target_resource: Path) -> None:
        chip = PrefixesChip()
        with open(origin_resource, "r") as origin:
            for line in origin:
                chip.lines.append(line.strip())
        with open(target_resource, "w") as target:
            for prefix in chip.prefixes:
                target.write(prefix + "\n")
