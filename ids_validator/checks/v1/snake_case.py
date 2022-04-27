from ids_validator.checks.abstract_checker import CheckResults, AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log

ignored_paths = [
    "root.properties.related_files.items.properties.pointer.properties.fileId",
    "root.properties.related_files.items.properties.pointer.properties.fileKey",
]

DEFINITIONS_PATH = "root.definitions"


class V1SnakeCaseChecker(AbstractChecker):
    def run(self, node: Node, context: dict = None) -> CheckResults:
        logs = []

        if node.path in ignored_paths or node.path.startswith(DEFINITIONS_PATH):
            return logs

        name: str = node.name
        checks = [
            name.islower() or name.isdigit(),
            len(name.split()) == 1,
            all([x.isalnum() for x in _filter_empty_string(name.split("_"))]),
        ]
        if not name.startswith("@") and not all(checks):
            logs.append(
                (f"'{node.name}' should be named as snake_case.", Log.CRITICAL.value)
            )

        return logs


def _filter_empty_string(str_list):
    return [str_val for str_val in str_list if str_val != ""]
