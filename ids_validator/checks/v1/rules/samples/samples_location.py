LOCATION = "root.properties.samples.items.properties.location"
POSITION = f"{LOCATION}.properties.position"
ROW = f"{LOCATION}.properties.row"
COLUMN = f"{LOCATION}.properties.column"
HOLDER = f"{LOCATION}.properties.holder"
HOLDER_NAME = f"{LOCATION}.properties.holder.properties.name"
HOLDER_TYPE = f"{LOCATION}.properties.holder.properties.type"
HOLDER_BARCODE = f"{LOCATION}.properties.holder.properties.barcode"

path_to_checks = {
    LOCATION: {
        "type": "object",
        "min_properties": ["position", "row", "column", "holder"],
    },
    POSITION: {"type": ["string", "null"]},
    ROW: {"type": ["number", "null"]},
    COLUMN: {"type": ["number", "null"]},
    HOLDER: {"type": "object", "min_properties": ["name", "type", "barcode"]},
    HOLDER_NAME: {"type": ["string", "null"]},
    HOLDER_TYPE: {"type": ["string", "null"]},
    HOLDER_BARCODE: {"type": ["string", "null"]},
}
