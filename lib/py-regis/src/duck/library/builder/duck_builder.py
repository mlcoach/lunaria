

from lib.builder.duck import Duck
from lib.abstractions.iduck import IDuck



class DuckBuilder(IDuck):
    """"""

    def __init__(self):
        self.duck = Duck()

    def set_fatal_fail_threshold(self, fatal_fail_threshold):
        self.duck.fatal_fail_threshold = fatal_fail_threshold
        return self

    def gather_services(self, service_list):
        self.duck.service_list = service_list
        for service in self.duck.service_list:
            service.fatal_fail_threshold = self.duck.fatal_fail_threshold
        return self

    def set_function(self, signal_as = None):
        self.duck.signal_as = signal_as
        return self

    def build(self):
        return self.duck
