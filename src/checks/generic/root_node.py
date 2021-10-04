from pydash import get

from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log

root_minimum_required = [
    "@idsType",
    "@idsVersion",
    "@idsNamespace"
]


class RootNodeChecker(AbstractChecker):

    def run(self, node: Node, context=None):
        logs = []
        if node.path == 'root':
            logs += RootNodeChecker._check_min_required_props(node)

            meta_paths = [
                f"properties.{name}"
                for name in root_minimum_required
            ]
            for path in meta_paths:
                prop = get(node, path)
                meta_checks = [
                    get(prop, "type") == 'string',
                    get(prop, "const")
                ]
                if not prop or not all(meta_checks):
                    logs.append(
                        (f"'{path}' must be of type 'string' with none-empty 'const'", Log.CRITICAL.value)
                    )
        return logs

    @staticmethod
    def _check_min_required_props(node: Node):
        logs = []
        if not node.has_required_list:
            logs.append(("'root.required' must be a list", Log.CRITICAL.value))

        if not node.required_contains_values(root_minimum_required):
            logs.append(
                (f"'required' must contain: {', '.join(sorted(root_minimum_required))}", Log.CRITICAL.value))

        return logs
