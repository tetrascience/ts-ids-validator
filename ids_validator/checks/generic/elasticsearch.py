import difflib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from ids_validator.checks.abstract_checker import AbstractChecker, CheckResults
from ids_validator.ids_node import Node
from ids_validator.utils import Log, read_schema


class ElasticsearchChecker(AbstractChecker):
    """
    - copy schema.json to temp folder
    - create elasticsearch.json in tmp folder
    - compare tmp/elasticsearch.json and ids/elasticsearch.json
    """

    def run(self, node: Node, context: dict = None) -> CheckResults:
        if node.path != "root":
            return []

        logs = []
        ids_dir: Path = context["ids_folder_path"]
        elasticsearch_json = ids_dir / "elasticsearch.json"
        convention_version = context.get("convention_version", "generic")

        criticality = (
            Log.WARNING.value if convention_version == "generic" else Log.CRITICAL.value
        )

        # Make sure elasticsearch.json exist
        if not elasticsearch_json.exists():
            logs += [
                (
                    f"Make sure elasticsearch.json exist at {elasticsearch_json}",
                    criticality,
                )
            ]
            return logs

        # Create a temp folder, copy ids/schema.json in it.
        # Generate a new elasticsearch.json in it
        try:
            with tempfile.TemporaryDirectory() as temp_ids_dir:
                shutil.copy(ids_dir / "schema.json", temp_ids_dir)
                self._create_new_elasticsearch_json(Path(temp_ids_dir))
                tmp_es_json = Path(temp_ids_dir) / "elasticsearch.json"
                original_es_schema = read_schema(elasticsearch_json)
                generated_es_schema = read_schema(tmp_es_json)
        except Exception as e:
            msg = f"ElasticsearchChecker: Internal Error: {repr(e)}"
            logs += [(msg, criticality)]
            return logs

        # Get ES mappings
        original_mapping = json.dumps(
            original_es_schema.get("mapping", {}), indent=2
        ).split("\n")
        generated_mapping = json.dumps(
            generated_es_schema.get("mapping", {}), indent=2
        ).split("\n")

        # Compare ES mappings
        diff_lines = difflib.unified_diff(
            original_mapping,
            generated_mapping,
            fromfile=str(elasticsearch_json),
            tofile=str(tmp_es_json),
        )
        diff_lines = list(diff_lines)
        if diff_lines:
            diff_lines = self._format_diffs(diff_lines)
            logs += [(diff_lines, criticality)]
        return logs

    def _create_new_elasticsearch_json(self, tmp: Path):
        subprocess.run(
            ["python", "-m", "ids_es_json_generator", str(tmp)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        tmp_es_json = tmp / "elasticsearch.json"
        if not tmp_es_json.exists():
            raise FileNotFoundError("Could not find generated elasticsearch.json")

    def _format_diffs(self, diffs):
        lines = [f"    {line}\n" for line in diffs]
        lines = ["Elasticsearch diff \n"] + lines
        return "".join(lines)
