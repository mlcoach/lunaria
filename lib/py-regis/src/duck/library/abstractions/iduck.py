from abc import ABCMeta, abstractmethod


class IDuck(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def set_fatal_fail_threshold():
        """fatal fail threshold for services"""
    @staticmethod
    @abstractmethod
    def gather_services():
        """service list that will be used for health check"""

    @staticmethod
    @abstractmethod
    def set_function():
        """signal type for health check(Fixed or Scheduled)"""

