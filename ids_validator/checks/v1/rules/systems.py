SYSTEMS = "root.properties.systems"
ITEMS = f"{SYSTEMS}.items"
ID = f"{SYSTEMS}.items.properties.id"
NAME = f"{SYSTEMS}.items.properties.name"
VENDOR = f"{SYSTEMS}.items.properties.vendor"
MODEL = f"{SYSTEMS}.items.properties.model"
TYPE = f"{SYSTEMS}.items.properties.type"
SERIAL_NUMBER = f"{SYSTEMS}.items.properties.serial_number"

FIRMWARE = f"{SYSTEMS}.items.properties.firmware"
FIRMWARE_ITEMS = f"{FIRMWARE}.items"
FIRMWARE_NAME = f"{FIRMWARE}.items.properties.name"
FIRMWARE_VERSION = f"{FIRMWARE}.items.properties.version"
FIRMWARE_LAST_UPDATE = f"{FIRMWARE}.items.properties.last_updated_timestamp"

SOFTWARE = f"{SYSTEMS}.items.properties.software"
SOFTWARE_ITEMS = f"{SOFTWARE}.items"
SOFTWARE_NAME = f"{SOFTWARE}.items.properties.name"
SOFTWARE_VERSION = f"{SOFTWARE}.items.properties.version"
SOFTWARE_SERIAL_NUMBER = f"{SOFTWARE}.items.properties.serial_number"
SOFTWARE_LAST_UPDATE = f"{SOFTWARE}.items.properties.last_updated_timestamp"

systems_rules = {
    SYSTEMS: {
        "type": "array",
        "min_properties": [
            "vendor",
            "model",
            "type",
        ],
    },
    ITEMS: {
        "type": "object",
        "min_required": ["vendor", "model", "type"],
    },
    ID: {"type": ["string", "null"]},
    NAME: {"type": ["string", "null"]},
    VENDOR: {"type": ["string", "null"]},
    MODEL: {"type": ["string", "null"]},
    TYPE: {"type": ["string", "null"]},
    SERIAL_NUMBER: {"type": ["string", "null"]},
    FIRMWARE: {
        "type": "array",
        "min_properties": [
            "name",
            "version",
        ],
    },
    FIRMWARE_ITEMS: {
        "type": "object",
        "min_required": ["name", "version"],
    },
    FIRMWARE_NAME: {"type": ["string", "null"]},
    FIRMWARE_VERSION: {"type": ["string", "null"]},
    FIRMWARE_LAST_UPDATE: {"type": ["string", "null"]},
    SOFTWARE: {
        "type": "array",
        "min_properties": [
            "name",
            "version",
        ],
    },
    SOFTWARE_ITEMS: {
        "type": "object",
        "min_required": ["name", "version"],
    },
    SOFTWARE_NAME: {"type": ["string", "null"]},
    SOFTWARE_VERSION: {"type": ["null", "string"]},
    SOFTWARE_LAST_UPDATE: {"type": ["string", "null"]},
}
