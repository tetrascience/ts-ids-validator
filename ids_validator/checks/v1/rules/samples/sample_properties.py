PROPERTIES = "root.properties.samples.items.properties.properties"
ITEMS = f"{PROPERTIES}.items"
SOURCE = f"{PROPERTIES}.items.properties.source"
SOURCE_NAME = f"{PROPERTIES}.items.properties.source.properties.name"
SOURCE_TYPE = f"{PROPERTIES}.items.properties.source.properties.type"
NAME = f"{PROPERTIES}.items.properties.name"
VALUE = f"{PROPERTIES}.items.properties.value"
VALUE_DATA_TYPE = f"{PROPERTIES}.items.properties.value_data_type"
STRING_VALUE = f"{PROPERTIES}.items.properties.string_value"
NUMERICAL_VALUE = f"{PROPERTIES}.items.properties.numerical_value"
NUMERICAL_VALUE_UNIT = f"{PROPERTIES}.items.properties.numerical_value_unit"
BOOLEAN_VALUE = f"{PROPERTIES}.items.properties.boolean_value"
TIME = f"{PROPERTIES}.items.properties.time"
TIME_LOOKUP = f"{PROPERTIES}.items.properties.time.properties.lookup"

path_to_checks = {
    ITEMS: {
        "type": "object",
        "required": [
            "source",
            "name",
            "value",
            "value_data_type",
            "string_value",
            "numerical_value",
            "numerical_value_unit",
            "boolean_value",
            "time",
        ],
    },
    SOURCE: {
        "type": "object",
        "required": ["name", "type"],
        "min_properties": ["name", "type"],
    },
    SOURCE_NAME: {"type": ["string", "null"]},
    SOURCE_TYPE: {"type": ["string", "null"]},
    NAME: {"type": "string"},
    VALUE: {"type": "string"},
    VALUE_DATA_TYPE: {"type": "string"},
    STRING_VALUE: {"type": ["string", "null"]},
    NUMERICAL_VALUE: {"type": ["number", "null"]},
    NUMERICAL_VALUE_UNIT: {
        "type": ["string", "null"],
    },
    BOOLEAN_VALUE: {"type": ["boolean", "null"]},
    TIME: {"type": "object", "required": ["lookup"], "min_properties": ["lookup"]},
    TIME_LOOKUP: {"type": ["string", "null"]},
}
