SYSTEMS = "root.properties.systems"
SYSTEMS_ITEMS = f"{SYSTEMS}.items"
SYSTEMS_ID = f"{SYSTEMS}.items.properties.id"
SYSTEMS_NAME = f"{SYSTEMS}.items.properties.name"
SYSTEMS_VENDOR = f"{SYSTEMS}.items.properties.vendor"
SYSTEMS_MODEL = f"{SYSTEMS}.items.properties.model"
SYSTEMS_TYPE = f"{SYSTEMS}.items.properties.type"
SYSTEMS_SERIAL_NUMBER = f"{SYSTEMS}.items.properties.serial_number"

SYSTEMS_FIRMWARE = f"{SYSTEMS}.items.properties.firmware"
SYSTEMS_FIRMWARE_ITEMS = f"{SYSTEMS_FIRMWARE}.items"
SYSTEMS_FIRMWARE_NAME = f"{SYSTEMS_FIRMWARE}.items.properties.name"
SYSTEMS_FIRMWARE_VERSION = f"{SYSTEMS_FIRMWARE}.items.properties.version"
SYSTEMS_FIRMWARE_LAST_UPDATE = f"{SYSTEMS_FIRMWARE}.items.properties.last_updated_timestamp"

SYSTEMS_SOFTWARE = f"{SYSTEMS}.items.properties.software"
SYSTEMS_SOFTWARE_ITEMS = f"{SYSTEMS_SOFTWARE}.items"
SYSTEMS_SOFTWARE_NAME = f"{SYSTEMS_SOFTWARE}.items.properties.name"
SYSTEMS_SOFTWARE_VERSION = f"{SYSTEMS_SOFTWARE}.items.properties.version"
SYSTEMS_SOFTWARE_SERIAL_NUMBER = f"{SYSTEMS_SOFTWARE}.items.properties.serial_number"
SYSTEMS_SOFTWARE_LAST_UPDATE = f"{SYSTEMS_SOFTWARE}.items.properties.last_updated_timestamp"

systems_rules = {
    SYSTEMS: {
        "type": "array",
        "min_properties": [
            "id",
            "name",
            "vendor",
            "model",
            "type",
            "serial_number",
            "firmware",
            "software"
        ]
    },
    SYSTEMS_ITEMS: {
        "type": "object",
        "min_required": [
            "vendor",
            "model",
            "type"
        ],

    },
    SYSTEMS_ID: {
        "type": ["string", "null"]
    },
    SYSTEMS_NAME: {
        "type": ["string", "null"]
    },
    SYSTEMS_VENDOR: {
        "type": ["string", "null"]
    },
    SYSTEMS_MODEL: {
        "type": ["string", "null"]
    },
    SYSTEMS_TYPE: {
        "type": ["string", "null"]
    },
    SYSTEMS_SERIAL_NUMBER: {"type": ["string", "null"]},

    SYSTEMS_FIRMWARE: {
        "type": "array",
        "min_properties": [
            "name",
            "version",
            "last_updated_timestamp"
        ]
    },
    SYSTEMS_FIRMWARE_ITEMS: {
        "type": "object",
        "min_required": [
            "name",
            "version"
        ],
    },
    SYSTEMS_FIRMWARE_NAME: {
        "type": ["string", "null"]
    },
    SYSTEMS_FIRMWARE_VERSION: {
        "type": ["string", "null"]
    },
    SYSTEMS_FIRMWARE_LAST_UPDATE: {
        "type": ["string", "null"]
    },

    SYSTEMS_SOFTWARE: {
        "type": "array",
        "min_properties": [
            "name",
            "version",
            "serial_number",
            "last_updated_timestamp"
        ]
    },
    SYSTEMS_SOFTWARE_ITEMS: {
        "type": "object",
        "min_required": [
            "name",
            "version"
        ],
    },
    SYSTEMS_SOFTWARE_NAME: {
        "type": ["string", "null"]
    },
    SYSTEMS_SOFTWARE_VERSION: {
        "type": ["string", "null"]
    },
    SYSTEMS_SOFTWARE_LAST_UPDATE: {
        "type": ["string", "null"]
    },
}
