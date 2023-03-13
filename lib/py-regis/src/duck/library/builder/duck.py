import threading
import asyncio
import time
import aioschedule as schedule
import aiohttp
from lib.abstractions.ihealth_funcs import IHealthFunc
from lib.health_dealing import HealthResult


class Duck():
    """Duck class for health check"""
    
    def __init__(self, fatal_fail_threshold=5, service_list=[],
                 signal_as = None) -> None:
        self.fatal_fail_threshold = fatal_fail_threshold
        self.service_list = service_list
        self.signal_as = signal_as
        self.thread = threading.Thread(target=self.start_health_check)
        self.thread.daemon = True
        self.thread.start()
        self._loop = asyncio.get_event_loop()
    def start_health_check(self):
        if self.signal_as == IHealthFunc.scheduled_heartbeat:
            self._scheduled_heartbeat()
        elif self.signal_as == IHealthFunc.fixed_heartbeat:
            self._fixed_heartbeat()
    def _scheduled_heartbeat(self):
        for service in self.service_list:
            schedule.every(service.time_interval).seconds.do(self._get_hearbeat, service)
        while True:
            self._loop.run_until_complete(schedule.run_pending())
            time.sleep(0.1)


    async def _get_hearbeat(self,service):
        async with aiohttp.ClientSession(trust_env=True) as session:    
            await asyncio.ensure_future(self._heartbeat(session, service))

    async def _heartbeat(self, session, service):
        async with session.get(service.url) as resp:
            response = await resp.json()
            if response['status']  == 'ok':
                service.succeed()
            else:
                service.failed(response.status_code)

    
    def _fixed_heartbeat(self):
        print("i m fixed")