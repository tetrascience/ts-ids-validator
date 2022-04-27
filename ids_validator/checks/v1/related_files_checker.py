from pathlib import Path

from ids_validator.checks.abstract_checker import AbstractChecker, CheckResults
from ids_validator.ids_node import Node
from ids_validator.utils import Log, read_schema

TEMPLATES_DIR = (Path(__file__) / "../../../templates").resolve()
RELATED_FILES_TEMPLATE = TEMPLATES_DIR / "related_files.json"
RELATED_FILES = "root.properties.related_files"


class V1RelatedFilesChecker(AbstractChecker):
    """
    Check that the related files schema matches the template from the schema conventions
    """

    def run(self, node: Node, context: dict = None) -> CheckResults:
        logs = []
        if node.path == RELATED_FILES:
            if not RELATED_FILES_TEMPLATE.exists():
                logs += [
                    (
                        f"Could not find template: {RELATED_FILES_TEMPLATE}",
                        Log.CRITICAL.value,
                    )
                ]
                return logs

            related_files_template = read_schema(RELATED_FILES_TEMPLATE)
            if related_files_template["related_files"] != node.data:
                logs += [
                    (
                        "'related_files' isn't an exact match of the template. Please "
                        "refer to the related files schema template documentation",
                        Log.CRITICAL.value,
                    )
                ]

        return logs
