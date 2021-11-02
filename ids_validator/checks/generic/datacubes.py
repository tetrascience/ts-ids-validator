from enum import Enum
from pydash import get

from ids_validator.checks import AbstractChecker
from ids_validator.ids_node import Node
from ids_validator.utils import Log

VALUE_NODE = "items.properties.measures.items.properties.value"
DIMENSION_NODE = "items.properties.dimensions"
SCALES_NODE = "items.properties.dimensions.items.properties.scale"


class Message(Enum):
    TYPE_CHECK = "'type' must be an array"
    REQUIRED_CHECK = "'required' must exist and contain at least ['name','measures','dimensions']"
    PROPERTY_CHECK = "'properties' must exist and contain all the required properties"
    MEASURES_UNDEFINED = "'measures' must be defined and 'measures.type' must be array"
    MEASURE_MIN_MAX_CHECK = "measures.minItems must be equal to measures.maxItems"
    MEASURE_MIN_MAX_MISSING = "'measures' must have both 'minItems' and 'maxItems' defined"
    DIMENSIONS_MIN_MAX_MISSING = "'dimension' must have both 'minItems' and 'maxItems' defined"
    DIMENSIONS_UNDEFINED = "'dimensions' must be defined and 'dimension.type' must be array"
    DIMENSIONS_MIN_MAX_CHECK = "dimensions.minItems must be equal to dimensions.maxItems"
    MEASURES_VALUES_DIMENSIONALITY_ERROR = "'measures.value': Dimensionality of data stored in `measures.value` must be equal to `dimesions.minItems` or `dimensions.maxItems`"
    MEASURES_VALUES_TYPE_ERROR = "'measures.value': Type Error. Type must be either be `number` or `string`. It can be nullable"
    MEASURES_VALUES_NESTED_ARRAY_TYPE_ERROR = "'measures.value': Type Error. Nested objects/dicts must be `array` types"
    DIMENSIONS_SCALE_TYPE_ERROR = "'dimensions.scale': Type Error. Type must be 'array'"
    DIMENSIONS_SCALE_ITEMS_TYPE_ERROR = "'dimensions.scale.items': Type Error. Type must be 'number'"

    def __str__(self):
        return self.value


class DatacubesChecker(AbstractChecker):
    """It run only when `node.path == "root.properties.datacubes"` and
    checks for following:
        - `type` of `datacubes` must be an array
        - Minimum required properties are present.
        - `minItems == maxItems` for `dimensions` and `measures`
        - Nesting levels of `measures.value` is equal to `dimensions.maxItem`
        - Type of nested levels must be an array except for the innermost array.
    """

    def run(self, node: Node, context: dict = None):
        logs = []
        if node.path == "root.properties.datacubes":
            logs += self.check_datacubes_type(node)
            logs += self.check_datacubes_properties(node)
            logs += self.check_datacubes_measures(node)
            logs += self.check_datacubes_dimensions(node)
            logs += self.check_measures_values_dimensions(node)
            logs += self.check_measures_values_type(node)
            logs += self.check_dimensions_scale_type(node)

        return logs

    @classmethod
    def check_datacubes_type(cls, datacubes):
        logs = []
        if get(datacubes, "type") != "array":
            logs += [(Message.TYPE_CHECK.value, Log.CRITICAL.value)]
        return logs

    @classmethod
    def check_datacubes_properties(cls, datacubes) -> list:
        """It checks for following:

        - `datacubes.items: dict` exists.
        - `required: list` must at least contain `minimum_properties`
        - `properties: dict` must at least contain `minimum_properties`

        where `minimum_properties = {'name', 'dimensions', 'measures'}`

        Args:
            datacubes (Node): Root level datacubes property

        Returns:
            list: list of failed check
        """
        logs = []
        items = datacubes.get("items")

        if not items or (type(items) != dict):
            logs += [
                (Message.REQUIRED_CHECK.value, Log.CRITICAL.value),
                (Message.PROPERTY_CHECK.value, Log.CRITICAL.value)
            ]
            return logs

        items = Node(items)
        minimum_required = {'name', 'dimensions', 'measures'}

        if not items.required_contains_values(minimum_required):
            logs += [(Message.REQUIRED_CHECK.value, Log.CRITICAL.value)]

        if not items.has_properties(list(minimum_required)):
            logs += [(Message.PROPERTY_CHECK.value, Log.CRITICAL.value)]

        return list(set(logs))

    @classmethod
    def check_datacubes_measures(cls, datacubes) -> list:
        """It checks for following:

        - `datacubes.measures` is defined in schema
        - `datacubes.measrues: dict` must contain `minItems`
        and `maxItems`
        - `measures.minItems` must be equal to `measures.maxItems`

        Args:
            datacubes (Node): Root level datacubes property

        Returns:
            list: list of failed check
        """
        logs = []
        measures = get(datacubes, "items.properties.measures")
        if not measures:
            logs += [(Message.MEASURES_UNDEFINED.value, Log.CRITICAL.value)]
            return logs

        if measures.get("type") != 'array':
            logs += [(Message.MEASURES_UNDEFINED.value, Log.CRITICAL.value)]

        minItems = get(measures, 'minItems')
        maxItems = get(measures, 'maxItems')

        if all([minItems, maxItems]):
            if minItems != maxItems:
                logs += [(Message.MEASURE_MIN_MAX_CHECK.value, Log.CRITICAL.value)]
        else:
            logs += [(Message.MEASURE_MIN_MAX_MISSING.value, Log.CRITICAL.value)]
        return list(set(logs))

    @classmethod
    def check_datacubes_dimensions(cls, datacubes) -> list:
        """It checks for following:

        - `datacubes.dimesions` is defined in schema
        - `datacubes.dimesions: dict` must contain `minItems`
        and `maxItems`
        - `dimesions.minItems` must be equal to `dimesions.maxItems`

        Args:
            datacubes (Node): Root level datacubes property

        Returns:
            list: list of failed check
        """
        logs = []
        dimensions = get(datacubes, "items.properties.dimensions")
        if not dimensions:
            logs += [(Message.DIMENSIONS_UNDEFINED.value, Log.CRITICAL.value)]
            return logs

        if dimensions.get('type') != 'array':
            logs += [(Message.DIMENSIONS_UNDEFINED.value, Log.CRITICAL.value)]

        minItems = get(dimensions, 'minItems')
        maxItems = get(dimensions, 'maxItems')

        if all([minItems, maxItems]):
            if minItems != maxItems:
                logs += [(Message.DIMENSIONS_MIN_MAX_CHECK.value, Log.CRITICAL.value)]
        else:
            logs += [(Message.DIMENSIONS_MIN_MAX_MISSING.value, Log.CRITICAL.value)]

        return list(set(logs))

    @classmethod
    def check_measures_values_dimensions(cls, datacubes: Node) -> list:
        """Ensures the nested depth of `measures.value` is equal to
        `dimensions.minItems` or `dimensions.maxItems`
        Args:
            datacubes (Node): Root level datacubes property

        Returns:
            list: list of failed check
        """
        logs = []
        values = get(datacubes, VALUE_NODE)
        dimensions = get(datacubes, DIMENSION_NODE)

        num_dimensions = (
            get(dimensions, "minItems")
            or get(dimensions, "maxItems")
        )
        if not (
            (values and type(values) == dict)
            and (dimensions and type(dimensions) == dict)
            and num_dimensions
        ):
            logs += [(Message.MEASURES_VALUES_DIMENSIONALITY_ERROR.value, Log.CRITICAL.value)]
            return logs

        value_dimensions = cls.get_value_dimensions(values)

        if num_dimensions != value_dimensions:
            logs += [(Message.MEASURES_VALUES_DIMENSIONALITY_ERROR.value, Log.CRITICAL.value)]

        return list(set(logs))

    @classmethod
    def check_measures_values_type(cls, datacubes: Node) -> list:
        """It makes sure that `measures.values` is a nested `dicts` of `array`,
        with innermost `dict` being a `number` or `string` type, nullable or not.

        Args:
            datacubes (Node): The root level datacubes property

        Returns:
            list: list of failed checks
        """
        logs = []
        values = Node(get(datacubes, VALUE_NODE) or {})
        error, msg = cls._check_measures_value_for_type_error(values)
        if error:
            logs += [(msg.value, Log.CRITICAL.value)]
        return logs

    @classmethod
    def check_dimensions_scale_type(cls, datacubes: Node) -> list:
        """Check type for `dimensions.scale`. It must be
        nested inside an `array` with type equals `number`

        Args:
            datacubes (Node): The root level datacubes property

        Returns:
            list: list of failed check
        """
        logs = []
        scale = get(datacubes, SCALES_NODE, {})
        if not scale:
            logs += [(Message.DIMENSIONS_SCALE_TYPE_ERROR.value, Log.CRITICAL.value)]

        if get(scale, "type") != "array":
            logs += [(Message.DIMENSIONS_SCALE_TYPE_ERROR.value, Log.CRITICAL.value)]

        valid_items_type =[
            "number",
            ["null", "number"],
            ["number", "null"]
        ]
        if get(scale, "items.type") not in valid_items_type:
            logs += [(Message.DIMENSIONS_SCALE_ITEMS_TYPE_ERROR.value, Log.CRITICAL.value)]

        return list(set(logs))

    @classmethod
    def get_value_dimensions(cls, node) -> int:
        """Calculate Depth of nesting only for `measures.value`.

        Args:
            node (dict): `dict` for `measures.value`

        Returns:
            int: Depth/dimensions of `measures.value`
        """

        node_items = get(node, "items")
        if node_items:
            return 1 + cls.get_value_dimensions(
                node_items,
            )
        return 0

    @classmethod
    def _check_measures_value_for_type_error(cls, node: dict) -> bool:
        """This is a helper function for valdating type of `measures.value`.
        It must be nested inside `array` types with innermost
        being either be a `number` or `string`, nullable or not.
        Args:
            node (dict): `measures.value`

        Returns:
            bool, Message: Return (False, None) if there is no error.
            Return (True, Message) in case validation fails
        """
        node_items = get(node, "items")
        node_type = get(node, "type")
        if node_items:
            if node_type != "array":
                return True, Message.MEASURES_VALUES_NESTED_ARRAY_TYPE_ERROR
            return cls._check_measures_value_for_type_error(node_items)
        else:
            if type(node_type) == list:
                if not(sorted(node_type) in [
                    sorted(["null", "string"]),
                    sorted(["null", "number"])
                ]):
                    return True, Message.MEASURES_VALUES_TYPE_ERROR
            elif node_type not in ["string", "number"]:
                return True, Message.MEASURES_VALUES_TYPE_ERROR

        return False, None
