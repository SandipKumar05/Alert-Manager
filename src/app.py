import os
import sys

from flask import Flask, jsonify, request

from src.config import PORT
from src.handler_factory import AlertHandlerFactory
from src.utils.logger import logger

app = Flask(__name__)


@app.route("/alert", methods=["POST"])
def receive_alert():
    try:
        alert = request.json
        logger.info(f"Received alert: {alert}")

        handler = AlertHandlerFactory.get_handler(alert)
        if handler:
            enriched_data = handler.enrich_data(alert)
            handler.take_action(enriched_data)

        return jsonify({"status": "received"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
