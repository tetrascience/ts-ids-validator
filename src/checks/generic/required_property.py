from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log


class RequiredPropertiesChecker(AbstractChecker):
    """If a node has defined `required: list` and `properties: dict`,
    this check makes sure, every value in `required` list is present in
    `properties.keys()`

    logs a failure if the check fails.
    """

    def run(self, node: Node, context: dict = None):
        logs = []
        if (
            node.has_required_list
            and not node.required_properties_exist
        ):
            logs.append(
                ("Required Properties are missing", Log.CRITICAL.value)
            )

        return logs
