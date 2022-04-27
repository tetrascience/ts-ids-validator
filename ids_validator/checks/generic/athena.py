import re
from pathlib import Path

from jsonschema import validate

from ids_validator.checks.abstract_checker import CheckResults, AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log, read_schema

TEMPLATES_DIR = (Path(__file__) / "../../../templates").resolve()
ATHENA_TEMPLATE = TEMPLATES_DIR / "athena.json"


class AthenaChecker(AbstractChecker):
    """Athena Checks run only at the root level of IDS Schema.
    It checks for following:
    - All the partition paths mentioned in `athena.js` are present in `schema.js`
    - Naming conflict between `path` and `name` of athena partition
    - Ancestor of any `partition.path` is not an array
    """

    def run(self, node: Node, context: dict = None) -> CheckResults:
        logs = []
        if node.name == "root":
            if not context.get("athena.json"):
                logs += [
                    (
                        "Make sure athena.js exist in IDS folder and has correct "
                        "structure.",
                        Log.CRITICAL.value,
                    )
                ]

            athena = context.get("athena.json")
            ids = context.get("schema.json")
            ids_node = Node(ids)

            logs += self._validate_schema(athena)
            if logs:
                return logs

            partition_paths = self.get_athena_partitions_path(athena)
            logs += self.check_all_paths_exist(partition_paths, ids_node)
            logs += self.check_paths_nested_inside_array(partition_paths, ids_node)
            logs += self.check_path_and_name_conflicts(athena)

        return logs

    @classmethod
    def check_all_paths_exist(cls, partition_paths: list, ids: Node):
        logs = []
        missing = [path for path in partition_paths if not cls.path_exists(path, ids)]
        if missing:
            logs.append(
                (
                    f"Athena.js: Cannot find following properties in IDS: "
                    f"{sorted(missing)}",
                    Log.CRITICAL.value,
                )
            )
        return logs

    @classmethod
    def check_paths_nested_inside_array(cls, partition_paths: list, ids: Node):
        logs = []
        existing_partition_paths = [
            path for path in partition_paths if cls.path_exists(path, ids)
        ]
        paths_nested_inside_array = sorted(
            [
                path
                for path in existing_partition_paths
                if cls.path_nested_in_array(path, ids)
            ]
        )
        if paths_nested_inside_array:
            logs.append(
                (
                    (
                        f"Athena.js: Following paths are either array type or nested "
                        f"in array types: {paths_nested_inside_array}"
                    ),
                    Log.CRITICAL.value,
                )
            )
        return logs

    @classmethod
    def check_path_and_name_conflicts(cls, athena_dict: dict):
        """Check and log if there is a conflict in `partition.path`
        and `partition.name`.

        A conflict occurs when normalized value of the `partition.path` is equal to
        `partition.name`.

        Normalized path is obtained by replacing "." with "_" in `partiions[*].path`

        Args:
            athena_dict (Node): athena.json loaded as a python dict
        """
        logs = []
        partitions_name = set(cls.get_athena_partitions_name(athena_dict))
        normalized_paths = set(
            [
                cls.normalize_path_name(path)
                for path in cls.get_athena_partitions_path(athena_dict)
            ]
        )
        intersection = partitions_name.intersection(normalized_paths)
        if intersection:
            logs.append(
                (
                    f"Athena.js: Following names are conflicting with path: "
                    f"{', '.join(intersection)}",
                    Log.CRITICAL.value,
                )
            )
        return logs

    @classmethod
    def path_nested_in_array(cls, path: str, ids: Node):
        """Traverse on node's path and return True if any
        ancestor is an array. Except if the ancestor is Top-Level
        IDS property.
        """
        nodes = path.split(".")
        parent = ids
        for idx, node in enumerate(nodes):
            children = parent.properties_dict
            child = children.get(node)
            if (parent["type"] == "array" and idx > 1) or (
                child["type"] == "array" and idx > 0
            ):
                return True

            parent = Node(child, path=None)
        return False

    @classmethod
    def path_exists(cls, path: str, ids: Node) -> bool:
        """Given a path eg `systems.firmwares.types`,
        make sure it exists in root level ids when crawled
        form properties to properties.

        Args:
            path (str): A fully qualified path, delimited by "."
            ids (Node): root IDS node

        Returns:
            bool: True if path exists else false
        """
        nodes = path.split(".")
        parent = ids
        for node in nodes:
            children = parent.properties_dict or {}
            child = children.get(node)
            if not child:
                return False
            parent = Node(child, path=None)
        return True

    @classmethod
    def get_athena_partitions_path(cls, athena_schema) -> list:
        partitions = athena_schema.get("partitions", {})
        paths = [partition.get("path") for partition in partitions]
        return paths

    @classmethod
    def get_athena_partitions_name(cls, athena_schema) -> list:
        partitions = athena_schema.get("partitions", {})
        names = [partition.get("name") for partition in partitions]
        return names

    @classmethod
    def normalize_path_name(cls, path_name):
        """
        Weird-partition!@name -> weird_partition_name
        @fileId -> fileid
        project.name -> project_name
        """
        normalized_path = re.sub("[^A-Za-z0-9]+", "_", path_name)
        normalized_path = re.sub("[_]+", "_", normalized_path)
        normalized_path = normalized_path.lstrip("_")
        normalized_path = normalized_path.lower()
        return normalized_path

    def _validate_schema(self, athena_schema):
        logs = []
        if not ATHENA_TEMPLATE.exists():
            logs += [
                (f"Could not find athena template : {ATHENA_TEMPLATE}", Log.CRITICAL)
            ]
            return logs

        template_schema = read_schema(ATHENA_TEMPLATE)
        try:
            validate(athena_schema, template_schema)
        except Exception as e:
            msg = str(e).split("\n")[0]
            logs += [(f"JSON schema validation failed : {msg}", Log.CRITICAL)]
        return logs
