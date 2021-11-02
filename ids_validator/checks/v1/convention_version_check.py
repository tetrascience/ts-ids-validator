from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log


class V1ConventionVersionChecker(AbstractChecker):
    def run(self, node: Node, context: dict):
        logs = []
        if node.path == 'root.properties.@idsConventionVersion':
            convention_version = context.get("convention_version")
            if node.get('const') != convention_version:
                logs.append(
                    (f"'@idsConventionVersion must be {convention_version}", Log.CRITICAL.value)
                )
        return logs