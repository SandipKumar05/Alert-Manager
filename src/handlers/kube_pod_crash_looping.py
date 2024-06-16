from src.handlers.alert_handler import AlertHandler
from src.utils.logger import logger
from src.utils.prometheus import fetch_cpu_usage, fetch_memory_usage
from src.utils.slack import send_message


class KubePodCrashLooping(AlertHandler):
    def enrich_data(self, alert):
        try:
            enriched_data = alert
            ns = alert.get("labels", {}).get("namespace")
            pod = alert.get("labels", {}).get("pod")
            container = alert.get("labels", {}).get("container")

            enriched_data["cpu_usage"] = fetch_cpu_usage(ns, pod, container)
            enriched_data["memory_usage"] = fetch_memory_usage(ns, pod, container)

            logger.info(f"added additional data")
            return enriched_data
        except Exception as e:
            logger.error(f"Error while adding data: {str(e)}")
            raise

    def take_action(self, alert):
        try:
            ns = alert.get("labels", {}).get("namespace")
            pod = alert.get("labels", {}).get("pod")
            cluster = alert.get("labels", {}).get("cluster")
            cpu_usage = alert.get("cpu_usage")
            memory_usage = alert.get("memory_usage")

            channel = alert.get("tags", {}).get("slack_channel")
            message = f""" Pod: {pod} is in crash looping state, namespace: {ns}, cluster: {cluster}
                        usage: CPU: {cpu_usage}, memory: {memory_usage} 
            """
            logger.info(f"slack to {channel} and {message}")
            send_message(channel, message)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise
