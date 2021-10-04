# ids-validator

TetraScience IDS Validator

* Each validation check should lead to a pass or fail
* Find as many failures as possible before terminating the validator, to make it easier to fix what’s wrong.
* Take definitions into account by using the "jsonref" library

## Generic Validations

### Summary

These validation steps apply to every IDS regardless of the designer because they are required by the platform.

### Rules

#### General

1. The required field `@idsType`, `@idsVersion`, `@idsNamespace` are included
2. `required` properties of an object are also defined in the object schema
3. `additionalProperties` is `false` for all objects
4. Fields with type `object` or `array` cannot also have a second type. Fields with any other type may have a second type of `null` only.
   * Allowed examples

    ```
    "type": "string"
    "type": ["string", "null"]
    "type": "number"
    "type": ["number", "null"]
    "type": "object"
    "type": "array"
    ```

   * Disallowed examples:

    ```
    "type": ["string", "number"]
    "type": ["number", "boolean"]
    "type": ["array", "null"]
    "type": ["array", "number"]
    "type": ["object", "null"]
    ```

5. **athena.json** partition path should be a valid path in schema.json (property is defined and cannot be in an array of object)
6. **athena.json** partition name should not conflict with path as defined in **athena.json** | Partition-Name

#### Datacubes

1. Validate that, if the datacubes field is present, it follows these parts of the datacubes pattern definition. Refer to the confluence page for the full detail.
2. The required `datacubes` fields are defined (`name`, `measures` and `dimensions`), their required fields are also defined
3. Check that `maxItems` = `minItems`, in both `datacubes[*].measures` and `datacubes[*].dimensions`
4. The shape of `measures[*].value` matches the number of dimensions (e.g. 2 dimensions → 2 layers of array in value)
5. Datacube values can only be numeric type not string type. This includes `measures[*].value` and `dimemsions[*].scale`

## TetraScience IDS Convention Validations

### Summary

These schema.json validation steps relate to TetraScience IDS convention. These will be checked in combination with the generic IDS validator.

If an IDS has `idsConventionVersion` field defined and is set to a version, then it must pass this TS IDS Convention Validation.

### Rules

#### IDS Convention v1.0.0

##### Error Cases

1. `@idsConventionVersion` is defined
2. The schema follows the IDS Fields definitions in ​. This will be the bulk of the work of this ticket. Try to make it extendable for when the IDS convention version changes.
3. The convention’s Required fields are present and follow the convention or template where specified.
4. All types follow the convention or templates, and are Not Null where specified.
5. All Non-Extendable objects don’t contain any fields other than the ones defined in the convention.
6. Field names match snake_case. No upper case characters, no whitespace, only alphanumeric and `_`
   * Note: Don’t do any spell checking or finding word boundaries - that will still be done manually by a reviewer

##### Warning Cases

1. Check that object names aren’t repeated in their child fields, e.g. `event.event_type` shouldn’t include `event_` in the child. Don’t fail the validation over this, only throw a warning so the reviewer can decide what to do
