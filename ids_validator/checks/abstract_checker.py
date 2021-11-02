from abc import ABCMeta, abstractmethod

from ids_validator.ids_node import Node


class AbstractChecker(metaclass=ABCMeta):
    @abstractmethod
    def run(self, node: Node, context: dict = None):
        raise NotImplementedError
