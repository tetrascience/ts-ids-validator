from enum import Enum


class Conventions(Enum):
    GENERIC = "generic"
    V1_0_0 = "v1.0.0"

    @staticmethod
    def get_by_value(convention_version):
        for convention in Conventions:
            if convention.value == convention_version:
                return convention

    @staticmethod
    def values():
        return sorted([convention.value for convention in Conventions])
