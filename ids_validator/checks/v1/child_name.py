from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


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
            logs += [(
                f"Child property prefix uses the same name as the parent property '{node.name}'",
                Log.WARNING.value
            )]
        return logs
