import asyncio
import threading
from collections.abc import Callable
import aioschedule as schedule
import time
import aiohttp
from abc import ABCMeta, abstractmethod
from lib.service import Service
from lib.builder.scheduled_duck import ScheduledDuck




if __name__ == '__main__':
    service_list = [Service(url = "http://localhost:8000/heartbeat", name = "Service", time_interval = 1, fail_threshold =  5),
                    Service(url = "http://localhost:8000/heartbeat", name = "Service", time_interval = 10, fail_threshold =  5),
                    Service(url = "http://localhost:8000/heartbeat", name = "Service", time_interval = 3, fail_threshold =  5),
                    Service(url = "http://localhost:8000/heartbeat", name = "Service", time_interval = 2, fail_threshold =  5)]


    ScheduledDuck.build(8, service_list).start_health_check()
