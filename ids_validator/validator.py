from pathlib import Path
from rich.console import Console

from ids_validator.ids_node import Node
from ids_validator.utils import Log


class Validator:
    def __init__(
        self,
        ids: dict,
        athena: dict,
        checks_list: list,
        convention_version: str,
        ids_folder_path: Path
    ):
        self.ids = ids
        self.athena = athena
        self.checks_list = checks_list
        self.context = {
            "athena.json": self.athena,
            "schema.json": self.ids,
            "convention_version": convention_version,
            "ids_folder_path": ids_folder_path
        }
        self.console = Console()
        self.property_failures = {}
        self.has_critical_failures = False

    def _traverse(self, schema, name="root", path="root"):
        node = Node(ids_dict=schema, name=name, path=path)

        failures = []
        for checker in self.checks_list:
            failures += checker.run(node, self.context)

        if failures:
            self.property_failures[node.path] = list(failures)
            self.log(failures, node.path)

        for k, v in schema.items():
            if type(v) == dict:
                self._traverse(v, name=k, path=f"{path}.{k}")

    def validate_ids(self):
        self._traverse(schema=self.ids)

    def log(self, messages, property_name, prop_color="red"):
        self.console.print(
            f"[b u  {prop_color}]{property_name}[/b u {prop_color}]:")

        for msg, log_level in sorted(messages, key=lambda x: str(x[0])):
            if log_level == Log.CRITICAL.value:
                self.has_critical_failures = True

            msg_color = "yellow" if log_level == Log.CRITICAL.value else "white"
            self.console.print(
                f"[italic {msg_color}]   * {msg}[italic {msg_color}]")
