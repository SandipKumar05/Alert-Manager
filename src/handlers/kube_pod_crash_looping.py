import json

from src.handlers.alert_handler import AlertHandler
from src.utils.k8s import delete_pod
from src.utils.logger import logger
from src.utils.prometheus import fetch_cpu_usage, fetch_memory_usage
from src.utils.slack import send_message


class KubePodCrashLooping(AlertHandler):
    def enrich_data(self, alert):
        try:
            enriched_data = alert
            enriched_data["cpu_usage"] = fetch_cpu_usage(alert)
            enriched_data["memory_usage"] = fetch_memory_usage(alert)

            logger.info(f"added additional data")
            return enriched_data
        except Exception as e:
            logger.error(f"Error while adding data: {str(e)}")
            raise

    def take_action(self, alert):
        try:
            # Deleting the pod
            pod_name = ""
            namespace = ""
            delete_pod(pod_name, namespace)

            # Notify the team about deletion
            channel = "#demo"
            message = ""
            send_message(channel, message)
            logger.info("action takes")
            logger.info(f"{alert}")
        except Exception as e:
            logger.error(f"Error while adding data: {str(e)}")
            raise
