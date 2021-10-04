from src.checks.v1.rules.samples.samples_root import path_to_checks as root_rules
from src.checks.v1.rules.samples.samples_locations import path_to_checks as locations_rules
from src.checks.v1.rules.samples.sample_properties import path_to_checks as properties_rules
from src.checks.v1.rules.samples.samples_labels import path_to_checks as labels_rules

samples_rules = {
    **root_rules,
    **locations_rules,
    **properties_rules,
    **labels_rules
}