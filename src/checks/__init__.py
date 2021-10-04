from src.checks.abstract_checker import AbstractChecker
from src.checks.generic import *
from src.checks.v1 import *
from src.convention_versions import Conventions

generic_checks = [
    AdditionalPropertyChecker(),
    AthenaChecker(),
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
    V1UserNodeChecker()
]


checks_dict = {
    Conventions.GENERIC: generic_checks,
    Conventions.V1_0_0 : v1_checks,
}
