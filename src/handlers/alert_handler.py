from abc import ABC, abstractmethod
class AlertHandler:
    @abstractmethod
    def enrich_data(self, alert):
        pass

    @abstractmethod
    def take_action(self, data):
        pass
