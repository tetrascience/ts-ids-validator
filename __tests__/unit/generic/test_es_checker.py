from pathlib import Path

import pytest

from src.checks import ElasticsearchChecker
from src.ids_node import Node
from src.utils import read_schema, Log


UNIT_TEST_FILES = Path("__tests__/unit/generic/files/elasticsearch")

dirs_to_expected = {
    "same_mapping": [],
    "different_mapping":[(
        (
            '             "audit_trail": {\n'
            '               "properties": {\n'
            '                 "injection": {\n'
            '    -              "properties": {}\n'
            '    +              "properties": {\n'
            '    +                "messages": {\n'
            '    +                  "type": "nested"\n'
            '    +                }\n'
            '    +              }\n'
            '                 },\n'
            '                 "data_item": {\n'
            '                   "properties": {\n'
        ),
        Log.WARNING.value
    )]
}


@pytest.mark.parametrize("test_dir,expected", dirs_to_expected.items())
def test_es_checker(test_dir, expected):
    ids_dir = UNIT_TEST_FILES / test_dir
    ids_dict = {
        "type":"object",
        "properties":{}
    }
    context = {
        "ids_folder_path": ids_dir,
        "convention_version": "generic"
    }

    elasticsearch_checker = ElasticsearchChecker()
    node = Node(name="root", ids_dict=ids_dict, path="root")
    logs = elasticsearch_checker.run(node, context)
    if logs:
        criticality = logs[0][1]
        msg = logs[0][0].split("\n")
        msg = '\n'.join(msg[7:])
        logs = [(msg, criticality)]
    assert sorted(logs) == sorted(expected)
