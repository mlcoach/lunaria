from enum import Enum


class HealthStatus(Enum):
    UNHEALTHY = 1
    HEALTHY = 2
    UNKOWN = 3


class HealthResult():
    def __init__(self, health_status, description) -> None:
        if health_status is None:
            health_status = HealthStatus.UNKOWN
        self.health_status = health_status
        if description is None:
            description = ""
        self.description = description
    @classmethod
    def healthy(self, description: str):
        return self(HealthStatus.HEALTHY, description)
    
    @classmethod
    def unhealthy(self, description: str):
        return self(HealthStatus.UNHEALTHY, description)

    @classmethod
    def unknown(self, description: str):
        return self(HealthStatus.UNKOWN, description)

class HealthRegistration:
    def __init__(self,
                 database_connection,) -> None:
        pass

    def register_health_status(self, service_url, health_status):
        pass

    def unregister(self, service_url):
        pass