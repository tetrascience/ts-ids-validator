from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log

class AdditionalPropertyChecker(AbstractChecker):
    """If a node has `additionalProperties`, it must be false.
    Log a message otherwise.
    """
    def run(self, node: Node, contex: dict = None):
        logs = []
        additional_properties = node.get("additionalProperties")
        if node._type != 'object' and additional_properties:
            logs.append(
                ("'additionalProperties' can only be defined for 'type = object'", Log.CRITICAL.value)
            )
        if additional_properties:
            logs.append(
                ("'additionalProperties' must be 'false'", Log.CRITICAL.value)
            )

        return logs
