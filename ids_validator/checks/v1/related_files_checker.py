import os
from pathlib import Path
from pydash import get
from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log, read_schema


RELATED_FILES_TEMPLATE = Path("templates/related_files.json")
RELATED_FILES = "root.properties.related_files"

class V1RelatedFilesChecker(AbstractChecker):
    def run(self, node: Node, context: dict):
        logs = []
        if node.path == RELATED_FILES:
            if not RELATED_FILES_TEMPLATE.exists():
                logs += [(
                    f"Could not find template: {RELATED_FILES_TEMPLATE}",
                    Log.CRITICAL.value
                )]
                return logs

            related_files_template = read_schema(RELATED_FILES_TEMPLATE)
            if related_files_template["related_files"] != node.data:
                logs += [(
                    "'related_files' isn't an exact match of the template. Please refer to confluence docs.",
                    Log.CRITICAL.value
                )]

        return logs
