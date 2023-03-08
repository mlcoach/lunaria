import threading
import time
import requests
from src.base import ServiceRegistration
STATE_OPEN = "open"
STATE_CLOSED = "closed"

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs) -> None:
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self) -> None:
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    
    def start(self) -> None:
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True
    
    def stop(self) -> None:
        self._timer.cancel()
        self.is_running = False


class ServiceStatus():
    def __init__(self,
                 service_url,
                 service_name,
                 state,
                 failure_treshold = 3,
                 timeout = 60) -> None:
        self.service_url = service_url
        self.service_name = service_name
        self.state = state
        self.failure_counter = 0
        self.last_failure_time  = None
        self.failure_threshold = failure_treshold
        self.timeout = timeout
    def send_heartbeat(self):
        print("Sending heartbeat to " + self.service_url)
        try:
            response = requests.get(self.service_url + "/heartbeat")
            if self.failure_counter < self.failure_threshold:    
                if response.status_code == 200:
                    print("Success")
                    self.failure_counter = 0
                    self.state = STATE_CLOSED
                else:
                    self.failure_counter += 1
                    self.last_failure_time = time.time()
            else: 
                if self.last_failure_time + self.timeout < time.time():
                    self.failure_counter += 0
                    self.send_heartbeat()
                else:
                    self.state = STATE_OPEN
        except Exception as e:
            self.failure_counter += 1
            self.last_failure_time = time.time()
            print(e)

class CircuitBreaker:
    def __init__(self,
                 services = {},
                 heartbeat_interval = 10,
                 service_registration : ServiceRegistration = None) -> None:                 
        self.services = services
        self.heartbeat_interval = heartbeat_interval
        self.service_registration = service_registration
        self.heartbeat_thread = RepeatedTimer(self.heartbeat_interval, self.send_heartbeats)
    def send_heartbeats(self):
        for service_url in self.services:
            self.services[service_url].send_heartbeat()
        for service_url in self.services:
            if self.services[service_url].state == STATE_CLOSED:
                self.service_registration.update_service("http://localhost:8000", 5)
    def get_service(self, service_name):
        for service_url in self.services:
            if self.services[service_url].service_name == service_name:
                return self.services[service_url]
        return None
    def get_services(self):
        return self.services
    def __exit__(self, exc_type, exc_value, traceback):
        self.heartbeat_thread.stop()

if __name__ == "__main__":
    service_registration = ServiceRegistration(host = 'localhost', port = '8080', scheme = 'http://')
    cb = CircuitBreaker({
        "http://localhost:8000": ServiceStatus("http://localhost:8000", "test", STATE_CLOSED),
        "http://localhost:8001": ServiceStatus("http://localhost:8001", "test", STATE_CLOSED),
    },
    10,
    service_registration)
    time.sleep(1)
