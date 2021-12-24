from abc import ABC, abstractmethod
from multiprocessing import Process


class Channel(ABC, Process):
    """
    ABC for channel object

    """
    test=True

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def shutdown(self):
        ...


