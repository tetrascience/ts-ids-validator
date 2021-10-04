from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log


class V1ChildNameChecker(AbstractChecker):
    """Checks if child name starts with parent's name"""

    def run(self, node: Node, context=None):
        logs = []
        properties = node.properties_list or []
        child_start_with_parent_name = [
            prop.lower().startswith(node.name.lower())
            for prop in properties
        ]
        if any(child_start_with_parent_name):
            logs.append(
                (f"Child property start with name '{node.name}'",
                 Log.WARNING.value)
            )
        return logs
