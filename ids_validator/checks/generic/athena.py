from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


class AthenaChecker(AbstractChecker):
    """Athena Checks run only at the root level of IDS Schema.
    It checks for following:
    - All the partition paths mentioned in `athena.js` are present in `schema.js`
    - Naming conflict between `path` and `name` of athena partition
    - Ancestor of any `partition.path` is not an array
    """

    def run(self, node: Node, context: dict = None):
        logs = []
        if node.name == "root":
            if not context.get("athena.json"):
                logs += [("Make sure athena.js exist in IDS folder and has correct structure.", Log.CRITICAL.value)]

            athena = context.get("athena.json")
            ids = context.get("schema.json")
            ids_node = Node(ids)
            partition_paths = self.get_athena_partitions_path(athena)

            logs += self.check_all_paths_exist(partition_paths, ids_node)
            logs += self.check_paths_nested_inside_array(
                partition_paths, ids_node)

            logs += self.check_path_and_name_conflicts(athena)
            logs += self.check_athena_path_and_root_properties_conflict(
                ids, athena)
        return logs

    @classmethod
    def check_all_paths_exist(cls, partition_paths: list, ids: Node):
        logs = []
        missing = [
            path
            for path in partition_paths
            if not cls.path_exists(path, ids)
        ]
        if missing:
            logs.append(
                (
                    f"Athena.js: Cannot find following properties in IDS: {sorted(missing)}",
                    Log.CRITICAL.value
                )
            )
        return logs

    @classmethod
    def check_paths_nested_inside_array(cls, partition_paths: list, ids: Node):
        logs = []
        existing_partition_paths = [
            path
            for path in partition_paths
            if cls.path_exists(path, ids)
        ]
        paths_nested_inside_array = sorted([
            path
            for path in existing_partition_paths
            if cls.path_nested_in_array(path, ids)
        ])
        if paths_nested_inside_array:
            logs.append(
                (
                    f"Athena.js: Following paths are either array type or nested in array types: {paths_nested_inside_array}",
                    Log.CRITICAL.value
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
        normalized_paths = set([
            path.replace(".", "_")
            for path in cls.get_athena_partitions_path(athena_dict)
        ])
        intersection = partitions_name.intersection(normalized_paths)
        if intersection:
            logs.append(
                (f"Athena.js: Following names are conflicting with path: {', '.join(intersection)}", Log.CRITICAL.value)
            )
        return logs

    @classmethod
    def check_athena_path_and_root_properties_conflict(cls, ids_dict, athena_dict):
        logs = []

        ids_top_level_props = set(ids_dict.get("properties", {}).keys())
        athena_normalized_paths = set([
            path.replace(".", "_")
            for path in cls.get_athena_partitions_path(athena_dict)
        ])

        intersection = ids_top_level_props.intersection(
            athena_normalized_paths)
        intersection = sorted(list(intersection))
        if intersection:
            logs.append(
                (f"Athena.js: Following athena paths are in conflict with top level properties in IDS schema: {intersection}", Log.CRITICAL.value)
            )

        return logs

    @classmethod
    def flatten_keys(cls, node: Node):
        result = []
        properties = node.properties_dict

        if not properties:
            return result

        for k, v in properties.items():
            sub_node = Node(v, path=None)
            sub_result = cls.flatten_keys(sub_node)

            if sub_result:
                sub_result = [k] + [
                    f"{k}.{prop}"
                    for prop in sub_result
                ]
                result += sub_result
            else:
                result += [k]

        return result

    @classmethod
    def path_nested_in_array(cls, path: str, ids: Node):
        nodes = path.split(".")
        parent = ids
        for idx, node in enumerate(nodes):
            children = parent.properties_dict
            child = children.get(node)
            if (
                (parent["type"] == 'array' and idx > 1)
                or (child["type"] == "array" and idx > 0)
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
        paths = [
            partition.get("path")
            for partition in partitions
        ]
        return paths

    @classmethod
    def get_athena_partitions_name(cls, athena_schema) -> list:
        partitions = athena_schema.get("partitions", {})
        names = [
            partition.get("name")
            for partition in partitions
        ]
        return names
