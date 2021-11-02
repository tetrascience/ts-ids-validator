from os import stat
from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log

class V1SnakeCaseChecker(AbstractChecker):
    def run(self, node: Node, context: dict = None):
        logs = []
        name: str = node.name
        checks = [
            name.islower() or name.isdigit(),
            len(name.split()) == 1,
            all(
                [
                    x.isalnum()
                    for x in _filter_empty_string(name.split('_'))
                ]
            )

        ]
        if not name.startswith("@") and not all(checks):
            logs.append(
                (f"'{node.name}' should be named as snake_case.", Log.CRITICAL.value)
            )

        return logs


def _filter_empty_string(str_list):
    return [
        str_val
        for str_val in str_list
        if str_val != ''
    ]
