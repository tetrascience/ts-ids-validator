from ids_validator.checks.abstract_checker import RUN_RETURN_TYPE, AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log
from pydash import get

CONVENTION_VERSION_PATH = "properties.@idsConventionVersion"


class V1RootNodeChecker(AbstractChecker):
    """
    Root node checker for V1.0.0 convention, checks only
    for the presence and correctness of `@idsConventionVersion`.
    It must be used in conjunction with generic RootNodeCheck.
    """

    def run(self, node: Node, context: dict) -> RUN_RETURN_TYPE:
        logs = []
        if node.path == "roots":
            convention_version = get(node, CONVENTION_VERSION_PATH)
            checks = [
                get(convention_version, "type") == "string",
                get(convention_version, "const"),
            ]
            if not convention_version or not all(checks):
                logs.append(
                    (
                        f"'{CONVENTION_VERSION_PATH}' must be of type 'string' with none-empty 'const'",
                        Log.CRITICAL.value,
                    )
                )

        return logs
