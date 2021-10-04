from collections import UserDict
from pydash import get


class Node(UserDict):

    def __init__(self, ids_dict, path=None, name="root"):
        self.data = ids_dict
        self.name = name
        self.path = path

    @property
    def properties_dict(self):
        ids = self.data
        if ids.get('type') == 'object' and ids.get('properties'):
            return ids.get('properties')
        elif ids.get('type') == 'array' and get(ids, 'items.properties'):
            return get(ids, 'items.properties')
        else:
            return None

    @property
    def properties_list(self):
        prop_dict = self.properties_dict
        if prop_dict:
            return prop_dict.keys()

    @property
    def _type(self):
        type = self.data.get('type')
        return type

    @property
    def has_required_list(self):
        required = self.get('required')
        required_exist = required and type(required) == list
        return True if required_exist else False

    def required_contains_values(self, values: list):
        if self.has_required_list:
            required = set(self.get('required'))
            min_required = set(values)
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
    def required_properties_exist(self):
        required = set(self.get("required"))
        properties = self.get("properties", {}).keys()
        if required.intersection(properties) != required:
            return False

        return True

    @property
    def has_valid_type(self):
        if self._type == 'object':
            return self._check_object_type()
        elif self._type == "array":
            return self._check_array_type()
        elif type(self._type) == list:
            return self._check_list_type()
        elif type(self._type) == str:
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
                "object Type must contain properties"
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

        # Otherwise, arrays must have child properties
        return (
            (True, None) if self.properties_list
            else (
                False,
                "'array' type must contain items.properties"
            )
        )

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
            (len(self._type) == 2),

            # array and object cannot be present
            # in list type
            ('array' not in self._type),
            ('object' not in self._type),

            # list must not contain same value
            not(all(x == self._type[0] for x in self._type)),

            # List must only contain values from
            # valid_nullable types
            ((set(self._type) - valid_nullable_types) == set()),
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
            (True, None) if self._type in valid_types
            else (False, None)
        )

    def _is_numeric_type(self):
        if type(self._type) == list:
            type_ = sorted(self._type)
            if not (
                type_ in [
                    sorted(["null", "integer"]),
                    sorted(["null", "number"])
                ]
            ):
                return False

        elif not(self._type in ["number", "integer"]):
            return False

        return True

    def get_missing_paths(self, paths: list):
        result = []
        for path in paths:
            if not get(self, path):
                result.append(path)
        return result
