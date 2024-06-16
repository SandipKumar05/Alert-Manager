from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config import SLACK_TOKEN
from src.utils.logger import logger

client = WebClient(token=SLACK_TOKEN)


def send_message(channel_id, message):
    logger.info(f"{channel_id}, {message}")
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        logger.debug(response)

    except SlackApiError as e:
        logger.error(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    send_message("#demo", "hello")
