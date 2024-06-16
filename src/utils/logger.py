import logging

from src.config import DEBUG

# Configure logger
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("alert_manager.log"), logging.StreamHandler()],
)


def get_logger(name):
    return logging.getLogger(name)
