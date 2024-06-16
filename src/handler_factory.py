from src.handlers.high_memory_usage import HighMemoryUsage
from src.handlers.kube_pod_crash_looping import KubePodCrashLooping
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AlertHandlerFactory:
    @staticmethod
    def get_handler(alert):
        alertname = alert.get("labels", {}).get("alertname")
        logger.info(f"alert name: {alertname}")
        if alertname == "KubePdCrashLooping":
            return KubePodCrashLooping()

        elif alertname == "HighMemoryUsage":
            return HighMemoryUsage()

        # add more handlers for different types here
        return None
