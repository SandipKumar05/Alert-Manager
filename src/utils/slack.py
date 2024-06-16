import json

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config import SLACK_TOKEN
from src.utils.logger import get_logger

logger = get_logger(__name__)
client = WebClient(token=SLACK_TOKEN)


def send_message(channel_id, message):
    if not SLACK_TOKEN:
        logger.error("Slack token not configured")
        raise ValueError("Slack token not configured")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_TOKEN}",
    }
    slack_data = {"channel": channel_id, "blocks": message["blocks"]}

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        data=json.dumps(slack_data),
    )
    if not response.ok:
        logger.error(f"Failed to send message to Slack: {response.text}")
        raise Exception(f"Failed to send message to Slack: {response.text}")

    logger.info("Message sent to Slack successfully")
