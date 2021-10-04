USERS = "root.properties.users"
USERS_ITEMS = f"{USERS}.items"
USERS_ID =  f"{USERS}.items.properties.id"
USERS_NAME = f"{USERS}.items.properties.name"
USERS_TYPE = f"{USERS}.items.properties.type"

user_rules = {
    USERS: {
        "type": "array",
        "min_properties": [
            "id",
            "name",
            "type"
        ]
    },
    USERS_ITEMS: {
        "type": "object",
    },
    USERS_ID: {
        "type": ["string", "null"]
    },
    USERS_NAME: {
        "type": ["string", "null"]
    },
    USERS_TYPE: {
        "type": ["string", "null"]
    }
}