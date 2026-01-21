from abc import ABC, abstractmethod
from datetime import datetime

class BaseScanner(ABC):
    def __init__(self, name):
        self.name = name
        self.results = []
        self.timestamp = datetime.now()

    @abstractmethod
    def run(self):
        pass
