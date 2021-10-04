LOCATION = "root.properties.samples.items.properties.location"
LOCATION_POSITION = f"{LOCATION}.properties.position"
LOCATION_ROW = f"{LOCATION}.properties.row"
LOCATION_COLUMN = f"{LOCATION}.properties.column"
LOCATION_HOLDER = f"{LOCATION}.properties.holder"
LOCATION_HOLDER_NAME = f"{LOCATION}.properties.holder.properties.name"
LOCATION_HOLDER_TYPE = f"{LOCATION}.properties.holder.properties.type"
LOCATION_HOLDER_BARCODE = f"{LOCATION}.properties.holder.properties.barcode"

path_to_checks = {
    LOCATION:{
        "type": "object",
        "min_properties": [
            "position",
            "row",
            "column",
            "holder"
        ]
    },
    LOCATION_POSITION: {
        "type": ["string", "null"]
    },
    LOCATION_ROW: {
        "type": ["number", "null"]
    },
    LOCATION_COLUMN: {
        "type": ["number", "null"]
    },
    LOCATION_HOLDER: {
        "type": "object",
        "min_properties": [
            "name",
            "type",
            "barcode"
        ]
    },
    LOCATION_HOLDER_NAME: {
        "type": ["string", "null"]
    },
    LOCATION_HOLDER_TYPE: {
        "type": ["string", "null"]
    },
    LOCATION_HOLDER_BARCODE: {
        "type": ["string", "null"]
    },
}