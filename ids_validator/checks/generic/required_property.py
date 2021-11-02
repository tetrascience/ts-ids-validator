from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


class RequiredPropertiesChecker(AbstractChecker):
    """If a node has defined `required: list` and `properties: dict`,
    this check makes sure, every value in `required` list is present in
    `properties.keys()`

    logs a failure if the check fails.
    """

    def run(self, node: Node, context: dict = None):
        logs = []
        if node.has_required_list:
            missing_properties = node.missing_properties
            if missing_properties:
                logs.append(
                    (f"Required Properties are missing: {missing_properties}", Log.CRITICAL.value)
                )

        return logs
