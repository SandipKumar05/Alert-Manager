import os

PORT = os.getenv("PORT", "5000")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
DEBUG = os.getenv("DEBUG", "False")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
