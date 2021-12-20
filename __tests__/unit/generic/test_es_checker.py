from pathlib import Path

import pytest
from pydash import get

from ids_validator.checks import ElasticsearchChecker
from ids_validator.ids_node import Node
from ids_validator.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/elasticsearch")

es_diff_str = (
    '             "audit_trail": {\n'
    '               "properties": {\n'
    '                 "injection": {\n'
    '    -              "properties": {}\n'
    '    +              "properties": {\n'
    '    +                "messages": {\n'
    '    +                  "type": "nested"\n'
    "    +                }\n"
    "    +              }\n"
    "                 },\n"
    '                 "data_item": {\n'
    '                   "properties": {\n'
)
dirs_to_expected = {
    "same_mapping": [],
    "different_mapping": [(es_diff_str, Log.CRITICAL.value)],
    "different_mapping_generic": [(es_diff_str, Log.WARNING.value)],
}


@pytest.mark.parametrize("test_dir,expected", dirs_to_expected.items())
def test_es_checker(test_dir, expected):
    ids_dir = UNIT_TEST_FILES / test_dir
    ids_schema = ids_dir / "schema.json"
    schema = read_schema(ids_schema)
    convention_version = get(
        schema, "properties.@idsConventionVersion.const", "generic"
    )
    ids_dict = {"type": "object", "properties": {}}
    context = {"ids_folder_path": ids_dir, "convention_version": convention_version}

    elasticsearch_checker = ElasticsearchChecker()
    node = Node(name="root", ids_dict=ids_dict, path="root")
    logs = elasticsearch_checker.run(node, context)
    if logs:
        criticality = logs[0][1]
        msg = logs[0][0].split("\n")
        msg = "\n".join(msg[7:])
        logs = [(msg, criticality)]
    assert sorted(logs) == sorted(expected)
