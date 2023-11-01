from abc import ABC, abstractmethod
import enum
from typing import List

from src.data.generic_data import GenericData


class HandlerMode(enum.Enum):
    READ = 1
    WRITE = 2
    APPEND = 3


class Handler(ABC):
    def __init__(
        self,
        name: str = None,
        mode: HandlerMode = HandlerMode.APPEND,
    ) -> None:
        self.name = name
        self.mode = mode

    def __repr__(self) -> str:
        return f"Handler(name={self.name}, mode={self.mode})"

    def __str__(self) -> str:
        return self.__repr__()

    @abstractmethod
    def handle(self, data: List[GenericData]):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_last(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_last_n(self, n: int):
        pass

    @abstractmethod
    def get_index(self, index: int):
        pass

    @staticmethod
    def get_handler(type: str):
        if type == "file":
            from src.handlers.file_handler import FileHandler

            return FileHandler

        if type == "console":
            from src.handlers.console_handler import ConsoleHandler

            return ConsoleHandler
