
from duck_builder import DuckBuilder
from lib.abstractions.ihealth_funcs import IHealthFunc


class FixedDuck:
    @staticmethod
    def build(fatal_fail_threshold, service_list):
        return DuckBuilder() \
            .set_fatal_fail_threshold(fatal_fail_threshold) \
            .gather_services(service_list) \
            .set_function(IHealthFunc.fixed_heartbeat) \
            .build()