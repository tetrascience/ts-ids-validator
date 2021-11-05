from collections import UserDict
from pydash import get


class Node(UserDict):

    def __init__(self, ids_dict, path="", name="root"):
        self.data = ids_dict
        self.name = name
        self.path = path

    @property
    def properties_dict(self):
        ids = self.data
        if ids.get('type') == 'object' and ids.get('properties') is not None:
            return ids.get('properties')
        elif ids.get('type') == 'array' and get(ids, 'items.properties') is not None:
            return get(ids, 'items.properties')
        else:
            return None

    @property
    def properties_list(self):
        prop_dict = self.properties_dict
        if prop_dict:
            return prop_dict.keys()

    @property
    def type_(self):
        type = self.data.get('type')
        return type

    @property
    def has_required_list(self):
        required = self.get('required')
        required_exist = required and type(required) == list
        return True if required_exist else False

    def required_contains_values(self, min_required_values: list):
        if self.has_required_list:
            required = set(self.get('required'))
            min_required = set(min_required_values)
            return (
                False if min_required - required
                else True
            )
        return False

    def has_properties(self, prop_list: list):
        properties = self.properties_list or []
        properties = set(properties)

        req_prop = set(prop_list)

        return (
            False
            if req_prop - properties
            else True
        )

    @property
    def missing_properties(self):
        required = set(self.get("required"))
        properties = self.get("properties", {}).keys()
        return required - properties

    @property
    def has_valid_type(self):
        if self.type_ == 'object':
            return self._check_object_type()
        elif self.type_ == "array":
            return self._check_array_type()
        elif type(self.type_) == list:
            return self._check_list_type()
        elif type(self.type_) == str:
            return self._check_unit_type()
        else:
            return True, None

    def _check_object_type(self):
        """Checks if `object` type contains properties

        Returns:
            tuple: A `tuple` with `boolean` that tells whether
            node a valid `object` type or not and a `string` message
            if its invalid `object` type
        """
        return (
            (True, None) if self.properties_list
            else (
                False,
                "'object' type must  contains non-empty 'properties'"
            )
        )

    def _check_array_type(self):
        """Checks if node is valid `array` type that contains
        child `properties`

        Returns:
            tuple: A `tuple` with `boolean` that tells whether
            node a valid `array` type or not and a `string` message
            if its invalid `array` type
        """
        # Arrays inside datacubes measures and dimensions
        # doesn't need to have children. So, ignore them.
        ignored_paths = [
            'datacubes.items.properties.measures',
            'datacubes.items.properties.dimensions',
        ]

        if (
            ignored_paths[0] in self.path
            or ignored_paths[1] in self.path
        ):
            return (True, None)

        # Array must contain items: dict
        if "items" not in self:
            return (False, "'array' type must contain 'items: dict'")

        items = get(self, "items")

        if not isinstance(items, dict):
            return (False, "'array' type must contain 'items: dict'")

        # Array must contain items.type
        # if type is invalid, it will picked up by validator
        # when checking items node
        if "type" not in items:
            return (False, "'array' type must contain items.type")

        # All Good, it a valid array time
        return True, None

    def _check_list_type(self):
        valid_nullable_types = {
            'number',
            'string',
            'boolean',
            'integer',
            'null'
        }

        checks = [
            # Length of list type must 2.
            (0 < len(self.type_) <= 2),

            # list must not contain same value
            len(set(self.type_)) == len(self.type_),

            # List must only contain values from
            # valid_nullable types
            ((set(self.type_) - valid_nullable_types) == set()),

            # If list contains two data types
            # make sure one of them is null
            (
                ("null" in self.type_)
                if len(self.type_) == 2
                else True
            ),

            # If list contains one datatypes
            # make sure its not null
            (
                ("null" not in self.type_)
                if len(self.type_) == 1
                else True
            )

        ]
        result = (
            (True, None) if all(checks)
            else (False, None)
        )
        return result

    def _check_unit_type(self):
        valid_types = {
            'number',
            'string',
            'boolean',
            'array',
            'object',
            'integer'
        }
        return (
            (True, None) if self.type_ in valid_types
            else (False, None)
        )

    def _is_numeric_type(self):
        if type(self.type_) == list:
            type_ = sorted(self.type_)
            if not (
                type_ in [
                    sorted(["null", "integer"]),
                    sorted(["null", "number"])
                ]
            ):
                return False

        elif not(self.type_ in ["number", "integer"]):
            return False

        return True

    def get_missing_paths(self, paths: list):
        result = []
        for path in paths:
            if not get(self, path):
                result.append(path)
        return result
