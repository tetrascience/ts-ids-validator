# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_generic_validators[generic_validator] 1'] = {
    'root': [
        (
            'Athena.js: Following names are conflicting with path: project_name',
            1
        ),
        (
            'Required Properties are missing',
            1
        ),
        (
            "'required' must contain: @idsNamespace, @idsType, @idsVersion",
            1
        ),
        (
            "'properties.@idsNamespace' must be of type 'string' with none-empty 'const'",
            1
        )
    ],
    'root.properties.datacubes': [
        (
            "'dimension' must have both 'minItems' and 'maxItems' defined",
            1
        ),
        (
            "'dimensions.scale': Type Error",
            1
        )
    ],
    'root.properties.results.items': [
        (
            "'additionalProperties' can only be defined for 'type = object'",
            1
        ),
        (
            "'additionalProperties' must be 'false'",
            1
        ),
        (
            'Required Properties are missing',
            1
        ),
        (
            "Invalid 'type': objects",
            1
        )
    ],
    'root.properties.results.items.properties.time': [
        (
            "Invalid 'type': nos",
            1
        )
    ]
}
