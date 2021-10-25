from src.convention_versions import Conventions
from src.checks.abstract_checker import AbstractChecker
from src.checks.generic import (
    AthenaChecker,
    AdditionalPropertyChecker,
    DatacubesChecker,
    RequiredPropertiesChecker,
    RootNodeChecker,
    TypeChecker,
)
from src.checks.v1 import (
    V1ChildNameChecker,
    V1ConventionVersionChecker,
    V1RootNodeChecker,
    V1SnakeCaseChecker,
    V1SampleNodeChecker,
    V1SystemNodeChecker,
    V1UserNodeChecker,
    V1RelatedFilesChecker
)

generic_checks = [
    AdditionalPropertyChecker(),
    DatacubesChecker(),
    RequiredPropertiesChecker(),
    RootNodeChecker(),
    TypeChecker()
]

v1_checks = generic_checks + [
    V1ChildNameChecker(),
    V1ConventionVersionChecker(),
    V1RootNodeChecker(),
    V1SnakeCaseChecker(),
    V1SampleNodeChecker(),
    V1SystemNodeChecker(),
    V1UserNodeChecker(),
    V1RelatedFilesChecker(),
]


checks_dict = {
    Conventions.GENERIC: generic_checks,
    Conventions.V1_0_0 : v1_checks,
}
