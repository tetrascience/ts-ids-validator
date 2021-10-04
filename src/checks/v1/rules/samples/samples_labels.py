LABELS = "root.properties.samples.items.properties.labels"
LABELS_ITEMS = f"{LABELS}.items"
LABELS_SOURCE = f"{LABELS}.items.properties.source"
LABELS_SOURCE_NAME = f"{LABELS}.items.properties.source.properties.name"
LABELS_SOURCE_TYPE = f"{LABELS}.items.properties.source.properties.type"
LABELS_NAME = f"{LABELS}.items.properties.name"
LABELS_VALUE = f"{LABELS}.items.properties.value"
LABELS_TIME = f"{LABELS}.items.properties.time"
LABELS_TIME_LOOKUP = f"{LABELS}.items.properties.time.properties.lookup"

path_to_checks = {
    LABELS_ITEMS: {
        "type": "object",
        "required": [
            "source",
            "name",
            "value",
            "time"
        ],
    },
    LABELS_SOURCE: {
        "type": "object",
        "required": [
            "name",
            "type"
        ],
        "min_properties": ["name", "type"]
    },
    LABELS_SOURCE_NAME: {
        "type": "string"
    },
    LABELS_SOURCE_TYPE: {
        "type":  ["string", "null"]

    },
    LABELS_NAME: {
        "type": "string"
    },
    LABELS_VALUE: {
        "type": "string"
    },
    LABELS_TIME: {
        "type": "object",
        "required": ["lookup"],
        "min_properties": ["lookup"]
    },
    LABELS_TIME_LOOKUP: {
        "type": ["string", "null"]
    }
}