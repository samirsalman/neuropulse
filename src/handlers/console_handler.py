from typing import List
from src.handlers.handler import Handler, HandlerMode
from src.app_logging.logger import logger
from src.data.generic_data import GenericData


class ConsoleHandler(Handler):
    def __init__(
        self, name: str = None, mode: HandlerMode = HandlerMode.APPEND, **kwargs
    ) -> None:
        super().__init__(name, mode)

    def handle(self, data: List[GenericData]):
        for d in data:
            logger.info(d.to_json())

    def clear(self):
        pass

    def get_last(self):
        pass

    def get_all(self):
        pass

    def get_last_n(self, n: int):
        pass

    def get_index(self, index: int):
        pass
