from ids_validator.checks.abstract_checker import CheckResults, AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log


class V1ConventionVersionChecker(AbstractChecker):
    def run(self, node: Node, context: dict = None) -> CheckResults:
        logs = []
        if node.path == "root.properties.@idsConventionVersion":
            convention_version = context.get("convention_version")
            if node.get("const") != convention_version:
                logs.append(
                    (
                        f"'@idsConventionVersion must be {convention_version}",
                        Log.CRITICAL.value,
                    )
                )
        return logs
