from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


class TypeChecker(AbstractChecker):
    """Checks if Node has a property `type` and
    is a valid JSON type or array of types
    """

    def run(self, node: Node, context: dict = None):
        logs = []
        type_is_valid, msg = node.has_valid_type
        if not type_is_valid:
            msg = msg if msg else f"Invalid 'type': {node.type_}"
            logs.append((msg, Log.CRITICAL.value))
        return logs
