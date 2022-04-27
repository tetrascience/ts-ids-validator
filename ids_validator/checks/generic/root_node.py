from ids_validator.checks.abstract_checker import CheckResults, AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log
from pydash import get

root_minimum_required = ["@idsType", "@idsVersion", "@idsNamespace"]


class RootNodeChecker(AbstractChecker):
    def run(self, node: Node, context=None) -> CheckResults:
        logs = []
        if node.path == "root":
            logs += RootNodeChecker._check_min_required_props(node)

            meta_paths = [f"properties.{name}" for name in root_minimum_required]
            for path in meta_paths:
                prop = get(node, path)
                meta_checks = [get(prop, "type") == "string", get(prop, "const")]
                if not prop or not all(meta_checks):
                    logs.append(
                        (
                            f"'{path}' must be present with type 'string' with "
                            f"non-empty 'const'",
                            Log.CRITICAL.value,
                        )
                    )

            if "type" not in node.data:
                logs += [("'root.type' is not defined.", Log.CRITICAL)]
            elif node.type_ != "object":
                logs += [
                    (
                        f"'root.type' is '{node.type_}'. It must be set to 'object'",
                        Log.CRITICAL,
                    )
                ]

        return logs

    @staticmethod
    def _check_min_required_props(node: Node):
        logs = []
        if not node.has_required_list:
            logs.append(("'root.required' must be a list", Log.CRITICAL.value))

        if not node.required_contains_values(root_minimum_required):
            logs.append(
                (
                    f"'required' must contain: "
                    f"{', '.join(sorted(root_minimum_required))}",
                    Log.CRITICAL.value,
                )
            )

        return logs
