from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


class AdditionalPropertyChecker(AbstractChecker):
    """If a node is object type, then it have additionalProperties
    defined as one of the key and it must be set to False

    If type is not object or is not defined, additionalProperties
    must not exist.
    """

    def run(self, node: Node, context: dict = None):
        logs = []

        if (
            node.get("type") != 'object'
            and "additionalProperties" in node
        ):
            logs.append(
                ("'additionalProperties' can only be defined for 'type = object'", Log.CRITICAL.value)
            )

        if (
            node.get("type") == 'object'
            and node.get("additionalProperties") is not False
        ):
            logs.append(
                ("'additionalProperties' must be present and set to 'false' for 'object' types", Log.CRITICAL.value)
            )

        return logs
