# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_generic_validators[generic_validator] 1'] = {
    'root': [
        (
            "Required Properties are missing: {'@idsNamespace'}",
            1
        ),
        (
            "'required' must contain: @idsNamespace, @idsType, @idsVersion",
            1
        ),
        (
            "'properties.@idsNamespace' must be present with type 'string' with non-empty 'const'",
            1
        )
    ],
    'root.properties.datacubes': [
        (
            "'dimension' must have both 'minItems' and 'maxItems' defined",
            1
        )
    ],
    'root.properties.results.items': [
        (
            "'additionalProperties' can only be defined for 'type = object'",
            1
        ),
        (
            "Required Properties are missing: {'id'}",
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
