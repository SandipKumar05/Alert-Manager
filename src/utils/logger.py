import logging

from src.config import DEBUG

logging.basicConfig(level=logging.INFO if not DEBUG else logging.DEBUG)

logger = logging.getLogger(__name__)
