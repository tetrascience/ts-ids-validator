import os
import subprocess
import pathlib
import shutil
import difflib
import json
import tempfile
from pathlib import Path
from distutils.dir_util import copy_tree
from src.ids_node import Node
from src.checks import AbstractChecker
from src.utils import Log, read_schema


class ElasticsearchChecker(AbstractChecker):
    """
    - copy schema.json to temp folder
    - create elasticsearch.json in tmp folder
    - compare tmp/elasticsearch.json and ids/elasticsearch.json
    """

    def run(self, node: Node, context: dict = None):
        if node.path != 'root':
            return []

        logs = []
        ids_dir: Path = context["ids_folder_path"]
        elasticsearch_json = ids_dir / "elasticsearch.json"
        convention_version = context.get("convention_version", "generic")

        criticality = (
            Log.WARNING.value
            if convention_version == "generic"
            else Log.CRITICAL.value
        )

        # Make sure elasticsearch.json exist
        if not elasticsearch_json.exists():
            logs += [(
                f"Make sure elasticsearch.json exist at {elasticsearch_json}",
                criticality
            )]
            return logs

        # Create a temp folder, copy ids/schema.json in it.
        # Generate a new elasticsearch.json in it
        try:
            with tempfile.TemporaryDirectory() as temp_ids_dir:
                shutil.copy(
                    str(ids_dir / "schema.json"),
                    temp_ids_dir
                )
                self._create_new_elasticsearch_json(Path(temp_ids_dir))
                tmp_es_json = Path(temp_ids_dir) / "elasticsearch.json"
                original_es_schema = read_schema(elasticsearch_json)
                generated_es_schema = read_schema(tmp_es_json)
        except Exception as e:
            logs += [(f"{str(e)}", criticality)]
            return logs

        # Get ES mappings
        original_mapping = json.dumps(
            original_es_schema.get("mapping", {}),
            indent=2
        ).split("\n")
        generated_mapping = json.dumps(
            generated_es_schema.get("mapping", {}),
            indent=2
        ).split("\n")

        # Compare ES mappings
        diff_lines = difflib.unified_diff(
            original_mapping,
            generated_mapping,
            fromfile=str(elasticsearch_json),
            tofile=str(tmp_es_json)
        )
        diff_lines = list(diff_lines)
        if diff_lines:
            diff_lines = self._format_diffs(diff_lines)
            logs += [(diff_lines, criticality)]
        return logs

    def _create_new_elasticsearch_json(self, tmp):
        try:
            cwd = pathlib.Path().resolve()
            es_generator = cwd / ".." / "ts-lib-protocol-script" / \
                "tools" / "elasticsearch_generator/main.py"
            if not es_generator.exists():
                raise Exception(
                    f"Could not find elasticsearch_generator: {es_generator}")
            es_gen_process = subprocess.run(
                ["python", str(es_generator), str(tmp)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            assert es_gen_process.returncode == 0, es_gen_process.stderr
            assert os.path.exists(
                tmp/"elasticsearch.json"), "Could not create tmp/elasticsearch.json"
        except Exception as e:
            msg = f"ElasticsearchChecker: Internal Error: {str(e)}"
            raise Exception(msg)

    def _format_diffs(self, diffs):
        lines = [
            f"    {line}\n"
            for line in diffs
        ]
        lines = ["Elasticsearch diff \n"] + lines
        return ''.join(lines)