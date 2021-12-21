USERS = "root.properties.users"
ITEMS = f"{USERS}.items"
ID = f"{USERS}.items.properties.id"
NAME = f"{USERS}.items.properties.name"
TYPE = f"{USERS}.items.properties.type"

users_rules = {
    USERS: {"type": "array", "min_properties": ["id", "name", "type"]},
    ITEMS: {
        "type": "object",
    },
    ID: {"type": ["string", "null"]},
    NAME: {"type": ["string", "null"]},
    TYPE: {"type": ["string", "null"]},
}
