from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from ids_validator.ids_node import Node
from ids_validator.utils import Log


CheckResults = List[Tuple[str, Log]]


class AbstractChecker(metaclass=ABCMeta):
    """The abstract definition of a node checker

    A checker contains a `run` method which runs checks on a node and produces check
    results. A concrete checker class can be made like this:

    ```
    class ConcreteChecker(AbstractChecker):
        def run(self, node: Node, context: dict = None) -> CheckResults:
            # check something about the node, given some context
            return []
    ```
    This checker class can then be added to a list of checks to run on a schema.
    """

    @abstractmethod
    def run(self, node: Node, context: dict = None) -> CheckResults:
        """Run this checker's checks on a node with a given context, returning the
        results of those checks
        """
        raise NotImplementedError
