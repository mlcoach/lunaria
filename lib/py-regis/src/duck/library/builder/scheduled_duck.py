
from lib.abstractions.ihealth_funcs import IHealthFunc
from lib.builder.duck_builder import DuckBuilder


class ScheduledDuck:
    @staticmethod
    def build(fatal_fail_threshold, service_list):
        return DuckBuilder() \
            .set_fatal_fail_threshold(fatal_fail_threshold) \
            .gather_services(service_list) \
            .set_function(IHealthFunc.scheduled_heartbeat) \
            .build()
        
    ...         
