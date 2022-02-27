import abc

from linebot import models


class LineMessageCreator(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> models.Message:
        pass
