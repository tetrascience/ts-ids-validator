from ids_validator.checks.v1.rules.samples.samples_root import path_to_checks as root_rules
from ids_validator.checks.v1.rules.samples.samples_location import path_to_checks as location_rules
from ids_validator.checks.v1.rules.samples.sample_properties import path_to_checks as properties_rules
from ids_validator.checks.v1.rules.samples.samples_labels import path_to_checks as labels_rules

samples_rules = {
    **root_rules,
    **location_rules,
    **properties_rules,
    **labels_rules
}