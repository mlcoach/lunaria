
import datetime
from lib.health_dealing import HealthResult, HealthStatus



class Service():

    """Service class is a wrapper for a service that is monitored by health checker."""

    FATAL_FAIL_THRESHOLD = 5


    def __init__(self,
                 name,
                 url,
                 time_interval,
                 fail_threshold) -> None:

        self.name = name
        self.url = url
        self.time_interval = time_interval
        self.fail_count = 0
        self.fail_threshold = fail_threshold
        self._health_result: HealthResult = HealthResult(
            HealthStatus.UNKOWN, None)
        self.last_failure_time = None
        self._old_time_interval = time_interval

    @property
    def health_result(self):
        return self._health_result

    @health_result.setter
    def health_result(self, health_result):
        self._health_result = health_result

    def is_healthy(self):
        return self.health_result.health_status == HealthStatus.HEALTHY

    def failed(self, status_code):
        
        if self.fail_count is None:
            self.health_result = HealthResult.unknown(
                "fail count is none service will not be used")

        else:
            self.fail_count += 1
            if self.fail_count >= self.fail_threshold and self.fail_count < self.FATAL_FAIL_THRESHOLD:
                self.last_failure_time = datetime.datetime.now()
                self.half_time_interval()
                self.health_result = HealthResult.unhealthy(
                    "fail threshold reached last failure time is set to {}".format(self.last_failure_time) + 
                    "response status code is {}".format(status_code))
            if self.fail_count == self.FATAL_FAIL_THRESHOLD:
                self.last_failure_time = datetime.datetime.now()
                self.health_result = HealthResult.unhealthy(
                    "\033[1;31;40m fatal fail threshold reached, service is unhealthy and it will be registred as unhealthy to database <-> " + 
                     "last failure time is set to {}".format(self.last_failure_time)) 


    def succeed(self):
        self.first_time_interval()
        self.fail_count = 0
        self.health_result = HealthResult.healthy("service is healthy")


    def half_time_interval(self):
        self.time_interval = self.time_interval / 2

    def first_time_interval(self):
        self.time_interval = self._old_time_interval