from typing import List, Union
from pydash import get

from ids_validator.ids_node import Node
from ids_validator.checks import AbstractChecker
from ids_validator.utils import Log


class RuleBasedChecker(AbstractChecker):
    def run(self, node: Node, context: dict = None):
        logs = []
        paths = list(self.rules.keys())
        if node.path in paths:
            checks = self.rules[node.path]
            if checks:
                logs += self.enforce_checks(node, checks)

        return logs

    @classmethod
    def enforce_checks(cls, node: Node, checks: dict):
        logs = []
        if "type" in checks:
            logs += cls.enforce_type(node, checks.get("type"))
        if "required" in checks:
            logs += cls.enforce_required(
                node,
                checks.get("required")
            )
        if "properties" in checks:
            logs += cls.enforce_properties(
                node,
                checks.get("properties")
            )
        if "min_properties" in checks:
            logs += cls.enforce_min_properties(
                node,
                checks.get("min_properties")
            )
        if "min_required" in checks:
            logs += cls.enforce_min_required(
                node, checks.get("min_required")
            )
        return logs

    @classmethod
    def enforce_type(cls, node: Node, type_: Union[List, str]):
        logs = []

        if type(node.type_) != type(type_):
            logs += [(f"'type' must be {type_}", Log.CRITICAL.value)]
            return logs
        elif (
            (type(type_) == list)
            and (sorted(node.type_) != sorted(type_))
        ):
            logs += [(f"'type' must be {type_}", Log.CRITICAL.value)]
        elif (
            (type(type_) != list)
            and (node.type_ != type_)
        ):
            logs += [(f"'type' must be {type_}", Log.CRITICAL.value)]

        return logs

    @classmethod
    def enforce_required(cls, node: Node, required: list):
        logs = []
        node_required = node.get("required")

        if node_required != required:
            logs += [(f"'required' must be {required}", Log.CRITICAL.value)]

        return logs

    @classmethod
    def enforce_min_required(cls, node: Node, required: list):
        logs = []
        min_required = set(required)
        node_required = node.get("required", [])
        if type(node_required) != list:
            logs += [(
                f"'required' must contain {min_required}",
                Log.CRITICAL.value
            )]
            return logs

        node_required = set(node_required)
        missing = min_required - node_required
        if missing:
            logs += [(
                f"'required' must contain {missing}",
                Log.CRITICAL.value
            )]

        return logs

    @classmethod
    def enforce_properties(cls, node: Node, properties: list):
        logs = []
        node_properties = (
            get(node, "properties")
            or get(node, "items.properties")
            or {}
        )
        node_properties = list(node_properties.keys())
        if sorted(node_properties) != sorted(properties):
            logs += [(
                f"'properties' must only contain {properties}",
                Log.CRITICAL.value
            )]

        return logs

    @classmethod
    def enforce_min_properties(cls, node: Node, properties: list):
        logs = []
        node_properties = (
            get(node, "properties")
            or get(node, "items.properties")
            or {}
        )
        node_properties = set(node_properties.keys())
        min_props = set(properties)

        missing = min_props - node_properties
        if missing:
            logs += [(
                f"'properties' must contain {sorted(list(missing))}",
                Log.CRITICAL.value
            )]
        return logs
