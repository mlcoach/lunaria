from abc import  abstractmethod
class IHealthFunc:
    @abstractmethod
    def scheduled_heartbeat():
        """scheduled Heartbeat"""
    @abstractmethod
    def fixed_heartbeat():
        """fixed Heartbeat"""