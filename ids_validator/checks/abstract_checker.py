from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from ids_validator.ids_node import Node
from ids_validator.utils import Log


RUN_RETURN_TYPE = List[Tuple[str, Log]]

class AbstractChecker(metaclass=ABCMeta):
    @abstractmethod
    def run(self, node: Node, context: dict = None) -> RUN_RETURN_TYPE:
        raise NotImplementedError
