LABELS = "root.properties.samples.items.properties.labels"
ITEMS = f"{LABELS}.items"
SOURCE = f"{LABELS}.items.properties.source"
SOURCE_NAME = f"{LABELS}.items.properties.source.properties.name"
SOURCE_TYPE = f"{LABELS}.items.properties.source.properties.type"
NAME = f"{LABELS}.items.properties.name"
VALUE = f"{LABELS}.items.properties.value"
TIME = f"{LABELS}.items.properties.time"
TIME_LOOKUP = f"{LABELS}.items.properties.time.properties.lookup"

path_to_checks = {
    ITEMS: {
        "type": "object",
        "required": [
            "source",
            "name",
            "value",
            "time"
        ],
    },
    SOURCE: {
        "type": "object",
        "required": [
            "name",
            "type"
        ],
        "min_properties": ["name", "type"]
    },
    SOURCE_NAME: {
        "type": "string"
    },
    SOURCE_TYPE: {
        "type":  ["string", "null"]

    },
    NAME: {
        "type": "string"
    },
    VALUE: {
        "type": "string"
    },
    TIME: {
        "type": "object",
        "required": ["lookup"],
        "min_properties": ["lookup"]
    },
    TIME_LOOKUP: {
        "type": ["string", "null"]
    }
}