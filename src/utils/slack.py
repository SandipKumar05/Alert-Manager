from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config import SLACK_TOKEN
from src.utils.logger import logger

client = WebClient(token=SLACK_TOKEN)


def send_message(channel_id, message):
    logger.info(channel_id, message)
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        logger.info(response)

    except SlackApiError as e:
        logger.erro(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    send_message("#demo", "abc")
