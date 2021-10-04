PROPERTIES = "root.properties.samples.items.properties.properties"
PROPERTIES_ITEMS = f"{PROPERTIES}.items"
PROPERTIES_SOURCE = f"{PROPERTIES}.items.properties.source"
PROPERTIES_SOURCE_NAME = f"{PROPERTIES}.items.properties.source.properties.name"
PROPERTIES_SOURCE_TYPE = f"{PROPERTIES}.items.properties.source.properties.type"
PROPERTIES_NAME = f"{PROPERTIES}.items.properties.name"
PROPERTIES_VALUE = f"{PROPERTIES}.items.properties.value"
PROPERTIES_VALUE_DATA_TYPE = f"{PROPERTIES}.items.properties.value_data_type"
PROPERTIES_STRING_VALUE = f"{PROPERTIES}.items.properties.string_value"
PROPERTIES_NUMERICAL_VALUE = f"{PROPERTIES}.items.properties.numerical_value"
PROPERTIES_NUMERICAL_VALUE_UNIT = f"{PROPERTIES}.items.properties.numerical_value_unit"
PROPERTIES_BOOLEAN_VALUE = f"{PROPERTIES}.items.properties.boolean_value"
PROPERTIES_TIME = f"{PROPERTIES}.items.properties.time"
PROPERTIES_TIME_LOOKUP = f"{PROPERTIES}.items.properties.time.properties.lookup"

path_to_checks = {
    PROPERTIES_ITEMS: {
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
            "time"
        ],
    },
    PROPERTIES_SOURCE: {
        "type": "object",
        "required": [
            "name",
            "type"
        ],
        "min_properties": ["name", "type"]
    },
    PROPERTIES_SOURCE_NAME: {
        "type": ["string", "null"]
    },
    PROPERTIES_SOURCE_TYPE: {
        "type":  ["string", "null"]
    },
    PROPERTIES_NAME: {
        "type": "string"
    },
    PROPERTIES_VALUE: {
        "type": "string"
    },
    PROPERTIES_VALUE_DATA_TYPE: {
        "type": "string"
    },
    PROPERTIES_STRING_VALUE: {
        "type": ["string", "null"]
    },
    PROPERTIES_NUMERICAL_VALUE: {
        "type": ["number", "null"]
    },
    PROPERTIES_NUMERICAL_VALUE_UNIT: {
        "type": ["string", "null"],
    },
    PROPERTIES_BOOLEAN_VALUE: {
        "type": ["boolean", "null"]
    },
    PROPERTIES_TIME: {
        "type": "object",
        "required": ["lookup"],
        "min_properties": ["lookup"]
    },
    PROPERTIES_TIME_LOOKUP: {
        "type": ["string", "null"]
    }
}

