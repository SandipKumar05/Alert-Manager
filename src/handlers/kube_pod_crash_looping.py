from src.handlers.alert_handler import AlertHandler
from src.utils.logger import get_logger
from src.utils.prometheus import fetch_cpu_usage, fetch_memory_usage
from src.utils.slack import send_message

logger = get_logger(__name__)


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
            channel = alert.get("tags", {}).get("slack_channel")
            message = self.create_slack_message(alert)
            send_message(channel, message)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise

    def create_slack_message(self, alert):
        description = alert["annotations"]["description"]
        summary = alert["annotations"]["summary"]
        labels = alert["labels"]
        action = "No action taken by alert manager"
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Alert:* {summary}\n*Description:* {description}",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Severity:*\n{labels.get('severity', 'N/A')}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Namespace:*\n{labels.get('namespace', 'N/A')}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Pod:*\n{labels.get('pod', 'N/A')}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Cluster:*\n{labels.get('cluster', 'N/A')}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*CPU Usage:*\n{alert.get('cpu_usage', 'N/A'):.2f}m",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Memory Usage:*\n{alert.get('memory_usage', 'N/A'):.2f}MB",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Action by Alert Manager:*\n{action}",
                        },
                    ],
                },
            ]
        }
