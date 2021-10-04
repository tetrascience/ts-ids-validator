SAMPLES = "root.properties.samples"
SAMPLES_ITEMS =  f"{SAMPLES}.items"
SAMPLES_ID = f"{SAMPLES}.items.properties.id"
SAMPLES_BARCODE = f"{SAMPLES}.items.properties.barcode"
SAMPLES_NAME = f"{SAMPLES}.items.properties.name"
SAMPLES_BATCH = f"{SAMPLES}.items.properties.batch"
SAMPLES_BATCH_ID = f"{SAMPLES}.items.properties.batch.properties.id"
SAMPLES_BATCH_NAME = f"{SAMPLES}.items.properties.batch.properties.name"
SAMPLES_BATCH_BARCODE = f"{SAMPLES}.items.properties.batch.properties.barcode"
SAMPLES_SET = f"{SAMPLES}.items.properties.set"
SAMPLES_SET_ID = f"{SAMPLES}.items.properties.set.properties.id"
SAMPLES_SET_NAME = f"{SAMPLES}.items.properties.set.properties.name"
SAMPLES_LOT = f"{SAMPLES}.items.properties.lot"
SAMPLES_LOT_ID = f"{SAMPLES}.items.properties.lot.properties.id"
SAMPLES_LOT_NAME = f"{SAMPLES}.items.properties.lot.properties.name"
SAMPLES_LOCATION = f"{SAMPLES}.items.properties.location"
SAMPLES_PROPERTIES = f"{SAMPLES}.items.properties.properties"
SAMPLES_LABELS = f"{SAMPLES}.items.properties.labels"


path_to_checks = {
    SAMPLES:{
        "type": "array",
    },
    SAMPLES_ITEMS:{
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
    SAMPLES_ID: {
        "type": ["string", "null"]
    },
    SAMPLES_BARCODE: {
        "type": ["string", "null"]
    },
    SAMPLES_NAME: {
        "type": ["string", "null"]
    },
    SAMPLES_BATCH: {
        "type": "object",
        "min_properties":[
            "id",
            "name",
            "barcode"
        ]
    },
    SAMPLES_BATCH_ID:{
        "type": ["string", "null"]
    },
    SAMPLES_BATCH_NAME: {
        "type": ["string", "null"]
    },
    SAMPLES_BATCH_BARCODE: {
        "type": ["string", "null"]
    },
    SAMPLES_SET: {
        "type": "object",
        "min_properties": [
            "id",
            "name"
        ]
    },
    SAMPLES_SET_ID:{
        "type": ["string", "null"]
    },
    SAMPLES_SET_NAME: {
        "type": ["string", "null"]
    },
    SAMPLES_LOT: {
        "type": "object",
        "min_properties": [
            "id",
            "name"
        ]
    },
    SAMPLES_LOT_ID: {
        "type": ["string", "null"]
    },
    SAMPLES_LOT_NAME: {
        "type": ["string", "null"]
    },
    SAMPLES_LOCATION: {
        "type" : "object"
    },
    SAMPLES_PROPERTIES: {
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
    SAMPLES_LABELS: {
        "type" : "array",
        "min_properties": [
            "source",
            "name",
            "value",
            "time"
        ],
    },
}