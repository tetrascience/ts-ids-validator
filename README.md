# TetraScience IDS Validator <!-- omit in toc -->

[![Build Status](https://app.travis-ci.com/tetrascience/ts-ids-validator.svg?branch=master)](https://app.travis-ci.com/tetrascience/ts-ids-validator)

## Table of Contents <!-- omit in toc -->

- [Overview](#overview)
- [Usage](#usage)
- [Components](#components)
  - [Node](#node)
  - [Checker Classes](#checker-classes)
  - [Validator](#validator)
  - [List of Checker Classes](#list-of-checker-classes)
    - [Base Classes](#base-classes)
    - [Generic](#generic)
    - [V1](#v1)
  - [Writing New Checks](#writing-new-checks)
  - [Extending Checkers Classes](#extending-checkers-classes)
    - [Pattern 1](#pattern-1)
    - [Pattern 2](#pattern-2)
  - [Running Checks for Specific Nodes](#running-checks-for-specific-nodes)
  - [List of Checks for Validator](#list-of-checks-for-validator)
- [Changelog](#changelog)
- [v0.9.11](#v0911)
- [v0.9.10](#v0910)
- [v0.9.9](#v099)
- [v0.9.8](#v098)
- [v0.9.7](#v097)
- [v0.9.6](#v096)

## Overview

TetraScience IDS Validator

- Each validation check should lead to a pass or fail
- Find as many failures as possible before terminating the validator, to make it easier to fix what’s wrong.
- Take definitions into account by using the "jsonref" library

The validator will validate these files in an IDS folder:

- schema.json
- elasticsearch.json
- athena.json (upcoming)

You can find the validation rules in:

- [IDS Design Conventions - schema.json](https://developers.tetrascience.com/docs/ids-design-conventions-schemajson)
- [IDS Design Conventions - elasticsearch.json](https://developers.tetrascience.com/docs/ids-design-conventions-elasticsearchjson)
- [IDS Design Conventions - athena.json](https://developers.tetrascience.com/docs/ids-design-conventions-athenajson)

## Usage

```bash
pipenv run python -m ids_validator --ids_dir=path/to/ids/folder
```

This will run the required checks for the `@idsConventionVersion` mentioned in `schema.json`.

If `@idsConventionVersion` is missing in `schema.json` or if it is not supported by `schema_validator`, only `generic` checks will be run.

## Components

### Node

- `Node: UserDict` class is an abstraction for `dict` in `schema.json`
- When crawling `schema.json`, each `key-value` pair where `value` is a `dict`, is casted into `Node` type.
- For each K_V pair, `Node` has following attributes
  - `name (default=root)`: The `key`
  - `data`: The `value:dict`
  - `path (default=root)`: The fully-qualified path for the `key` in `schema.json`
- File: [ids_node.py](src/ids_node.py)

### Checker Classes

- A checker class must implement `AbstractChecker`
- When crawling `schema.json`, its `run()` method will be called for each node.
- `run()` implements the rules/condition to be checked for validating the node.
- `run()` accepts two arguments:
  - `node: Node`: `Node` for which we are running the checks
  - `context: dict`
    - It contains python dicts for `schema.json`, `athena.json` and `convention_version`.
    - It is used to supplementary data required for running complex checks.

### Validator

- `Validator` class is the one that implements the crawler.
- It has following attributes:
  - `ids: dict`: `schema.json` converted to python `dict`
  - `athena: dict`: `athena.json` converted to python `dict`
  - `checks_list`: A list of instantiated checker classes.
    These list of checks will be run for each node
- `Validator.traverse_ids()` crawls from `Node` to `Node` in `ids:dict`, Calling `run()` for each checker in the checks_list on the node

### List of Checker Classes

#### Base Classes

- `AbstractChecker`

  - Every checker class must implement it.
  - File: [abstract_checker.py](src/checks/abstract_checker.py)

- `RuleBasedChecker`
  - It is base class that allows validating `Node` against a set of `rules`
  - It comes in handy for implementing checks for property Nodes that has predefined template
  - The child class inheriting `RulesBasedChecker` must define `rules`
  - `rules` is a `dict` that maps `Node.path` to `set of rules:dict`
  - The `set of rules` for a `Node.path` may contain following keys:
    - `type: str`: defines what should be the `type` value for the `Node`
    - `min_properties: list`: defines minimum set of property names, that must exist for the Node. More properties can exist in addition to `min_properties`
    - `properties: list`: defines a set of property names that must must exactly match the property list of the `Node`
    - `min_required: list`: The required list of the `Node` must at least contain the values mentioned in `min_required`
    - `required: list`: The required list of the `Node` must only contain values listed in `required`
- Rules based checkers defined for v1 conventions can be found [here](src/checks/v1/nodes_checker.py)

#### Generic

- `AdditionalPropertyChecker`: [additional_property.py](src/checks/generic/additional_property.py)
- `RequiredPropertiesChecker`: [required_property.py](src/checks/generic/required_property.py)
- `DatacubesChecker`: [datacubes.py](src/checks/generic/datacubes.py)
- `RootNodeChecker`: [root_node.py](src/checks/generic/root_node.py)
- `TypeChecker`: [type_check.py](src/checks/generic/type_check.py)
- `AthenaChecker`: [athena.py](src/checks/generic/athena.py)

#### V1

- `V1ChildNameChecker`: [child_name.py](src/checks/v1/child_name.py)
- `V1ConventionVersionChecker`: [convention_version_check.py](src/checks/v1/convention_version_check.py)
- `V1SystemNodeChecker`: [nodes_checker.py](src/checks/v1/nodes_checker.py)
- `V1SampleNodeChecker`: [nodes_checker.py](src/checks/v1/nodes_checker.py)
- `V1UserNodeChecker`: [nodes_checker.py](src/checks/v1/nodes_checker.py)
- `V1RootNodeChecker`: [root_node.py](src/checks/v1/root_node.py)
- `V1SnakeCaseChecker`: [snake_case.py](src/checks/v1/snake_case.py)

### Writing New Checks

- Checkers must implement `AbstractCheckers`
- `run()` method implement one or more checks for the node
- In case of no failure an empty list must be returned
- In case of failures, it must return a list of one or more tuple
- The tuple will contain two values
  - `log message:str`: The message to be logged when check fails
  - `criticality`: either `Log.CRITICAL` or `Log.WARNING`

### Extending Checkers Classes

#### Pattern 1

```python
class ChildChecker(ParentChecker):
    def run(node: Node, context: dict):
        logs = []
        # Implement new checks and append failure to logs

        # Run Parent checkers and append logs
        logs += super().run(node, context)
        return logs
```

If `check_list` passed to `Validator` contains the `ChildChecker`, then it must not contain `ParentChecker` in the same list.
Doing so will cause ParentCheck to run twice and populate failures logs if any, twice.

TODO: Instead of `return logs`, we can `return set(logs)` to remove duplicates, but we cannot avoid executing same code twice

#### Pattern 2

```python
class ChildChecker(ParentChecker):
    def run(node: Node, context: dict):
        logs = []
        # Implement new checks and append failure to logs
        # use or override helper function of the parent class
        return logs
```

### Running Checks for Specific Nodes

```python
class AdhocChecker(AbstractChecker):
    def run(node: Node, context: dict):
        logs = []
        paths = []
        # paths is a list of fully qualified path to a key in schema.json
        # each path must start form root
        # eg: root.samples
        # eg: root.samples.items.properties.property_name
        if node.path in  paths:
            # Implement new checks and append failure to logs
            logs += perform_new_checks(node, context)
        return logs
```

### List of Checks for Validator

- `checks_dict`, defined [here](src/checks/__init__.py), maps the `type of validation` that we want to perform to the `list the of checks` needed to be run for the validation
- The list off checks is actually a list of instantiated checker objects

## Changelog

## v0.9.11

- Fix bug in `AthenaChecker` to allow root level IDS properties as partition paths.
- Update `TypeChecker` to catch errors related to undefined/misspelled `type` key.
- Update `jsonschema` version to fix package installation error

## v0.9.10

- Modify `V1SnakeCaseChecker` to ignore checks for keys present in `definitions` object.
- Add temporary allowance for `@link` in `*.properties`

## v0.9.9

- Lock `jsonschema` version in requirements.txt

## v0.9.8

- Modify `RulesChecker` to log missing and extra properties

## v0.9.7

- Allow properties with `const` values to have non-nullable `type`

## v0.9.6

- Add checker classes for generic validation
- Add checker classes for v1.0.0 convention validation
