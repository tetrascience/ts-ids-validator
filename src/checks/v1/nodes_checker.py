from src.checks.v1.rules.samples import samples_rules
from src.checks.v1.rules.systems import systems_rules
from src.checks.v1.rules.users import user_rules
from src.checks.rules_checker import RuleBasedChecker


class V1SystemNodeChecker(RuleBasedChecker):
    rules = systems_rules


class V1SampleNodeChecker(RuleBasedChecker):
    rules = samples_rules


class V1UserNodeChecker(RuleBasedChecker):
    rules = user_rules
