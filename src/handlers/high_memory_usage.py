from src.handlers.alert_handler import AlertHandler
from src.utils.k8s import delete_pod
from src.utils.logger import logger
from src.utils.prometheus import fetch_memory_usage
from src.utils.slack import send_message


class HighMemoryUsage(AlertHandler):
    def enrich_data(self, alert):
        try:
            enriched_data = alert
            ns = alert.get("labels", {}).get("namespace")
            pod = alert.get("labels", {}).get("pod")
            container = alert.get("labels", {}).get("container")

            logger.info("Fetching the memory usage")
            enriched_data["memory_usage"] = fetch_memory_usage(ns, pod, container)
            logger.info(f"added memory usage data")
            return enriched_data
        except Exception as e:
            logger.error(f"Error while adding data: {str(e)}")
            raise

    def take_action(self, alert):
        try:
            ns = alert.get("labels", {}).get("namespace")
            pod = alert.get("labels", {}).get("pod")
            cluster = alert.get("labels", {}).get("cluster")
            logger.info(f"Restarting the pod: {pod}, namespace: {ns}")
            delete_pod(pod, ns)

            # Notify the team about deletion
            channel = alert.get("tags", {}).get("slack_channel")
            message = f"""Pod: {pod} is using too much memory, 
            namespace: {ns}, cluster: {cluster}
            Restarted the pod to fix the issue
            """
            logger.info(f"slack to {channel} and {message}")
            send_message(channel, message)
        except Exception as e:
            logger.error(f"Error while adding data: {str(e)}")
            raise
