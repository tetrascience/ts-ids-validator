SAMPLES = "root.properties.samples"
ITEMS =  f"{SAMPLES}.items"
ID = f"{SAMPLES}.items.properties.id"
BARCODE = f"{SAMPLES}.items.properties.barcode"
NAME = f"{SAMPLES}.items.properties.name"
BATCH = f"{SAMPLES}.items.properties.batch"
BATCH_ID = f"{SAMPLES}.items.properties.batch.properties.id"
BATCH_NAME = f"{SAMPLES}.items.properties.batch.properties.name"
BATCH_BARCODE = f"{SAMPLES}.items.properties.batch.properties.barcode"
SET = f"{SAMPLES}.items.properties.set"
SET_ID = f"{SAMPLES}.items.properties.set.properties.id"
SET_NAME = f"{SAMPLES}.items.properties.set.properties.name"
LOT = f"{SAMPLES}.items.properties.lot"
LOT_ID = f"{SAMPLES}.items.properties.lot.properties.id"
LOT_NAME = f"{SAMPLES}.items.properties.lot.properties.name"
LOCATION = f"{SAMPLES}.items.properties.location"
PROPERTIES = f"{SAMPLES}.items.properties.properties"
LABELS = f"{SAMPLES}.items.properties.labels"


path_to_checks = {
    SAMPLES:{
        "type": "array",
    },
    ITEMS:{
        "type": "object",
        "properties":[
            "id",
            "barcode",
            "name",
            "batch",
            "set",
            "lot",
            "location",
            "properties",
            "labels"
        ]
    },
    ID: {
        "type": ["string", "null"]
    },
    BARCODE: {
        "type": ["string", "null"]
    },
    NAME: {
        "type": ["string", "null"]
    },
    BATCH: {
        "type": "object",
        "min_properties":[
            "id",
            "name",
            "barcode"
        ]
    },
    BATCH_ID:{
        "type": ["string", "null"]
    },
    BATCH_NAME: {
        "type": ["string", "null"]
    },
    BATCH_BARCODE: {
        "type": ["string", "null"]
    },
    SET: {
        "type": "object",
        "min_properties": [
            "id",
            "name"
        ]
    },
    SET_ID:{
        "type": ["string", "null"]
    },
    SET_NAME: {
        "type": ["string", "null"]
    },
    LOT: {
        "type": "object",
        "min_properties": [
            "id",
            "name"
        ]
    },
    LOT_ID: {
        "type": ["string", "null"]
    },
    LOT_NAME: {
        "type": ["string", "null"]
    },
    LOCATION: {
        "type" : "object"
    },
    PROPERTIES: {
        "type" : "array",
        "min_properties":[
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
    LABELS: {
        "type" : "array",
        "min_properties": [
            "source",
            "name",
            "value",
            "time"
        ],
    },
}