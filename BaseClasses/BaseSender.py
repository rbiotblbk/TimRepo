from abc import ABC, abstractmethod


class Sender(ABC):
    @abstractmethod
    def get_config(self) -> bool:
        pass

    @abstractmethod
    def send(self) -> None:
        pass
