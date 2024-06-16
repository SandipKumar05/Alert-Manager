# Alert Manager

# Alert Manager

## Overview

Alert Manager is a system designed to handle alerts programmatically with defined actions. The system can receive alerts via a webhook, enrich the data, and take appropriate actions based on the alert type. It is designed for easy extendability, allowing developers to add new alert types and handling pipelines.

## Features

- **Receive Alerts**: Webhook endpoint to receive alerts.
- **Enrich Data**: Enrich alert data by fetching additional information.
- **Take Action**: Execute actions such as sending notifications to Slack based on the alert.
- **Extendability**: Easily add new alert types and handling pipelines.


## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/alert_manager.git
cd alert_manager

# install dependencies
pip install -r requirements.txt

# export env variable as per src/config.py file
export SLACK_TOKEN=<your slack app token>
export PORT=5000
# Add path in PYTHONPATH variable
export PYTHONPATH="${PYTHONPATH}:/path/to/repo"
# Execute entry point
python src/app.py

# The application will be accessible at http://localhost:5000
```

## Example post request

```bash
curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -d '{
           "annotations": {
             "description": "Pod customer/customer-rs-transformer-9b75b488c-cpfd7 (rs-transformer) is restarting 2.11 times / 10 minutes.",
             "summary": "Pod is crash looping."
           },
           "labels": {
             "alertname": "KubePodCrashLooping",
             "cluster": "cluster-main",
             "container": "rs-transformer",
             "endpoint": "http",
             "job": "kube-state-metrics",
             "namespace": "customer",
             "pod": "customer-rs-transformer-9b75b488c-cpfd7",
             "priority": "P0",
             "prometheus": "monitoring/kube-prometheus-stack-prometheus",
             "region": "us-west-1",
             "replica": "0",
             "service": "kube-prometheus-stack-kube-state-metrics",
             "severity": "CRITICAL"
           },
           "startsAt": "2022-03-02T07:31:57.339Z",
           "status": "firing"
         }'

```


## Adding New Alert Handlers workflow

To add support for new alert types and handling pipelines in the Alert Manager system, follow these steps:

### 1. Create a New Handler Class

1.1. Create a new file in the `src/handlers` directory, for example, `new_alert_handler.py`:

```python
# src/handlers/new_alert_handler.py

from src.handlers.base import AlertHandler
from src.utils.logger import logger

class NewAlertHandler(AlertHandler):
    def enrich_data(self, alert):
        try:
            enriched_data = alert
            enriched_data["additional_info"] = "Fetched additional data for new alert"
            logger.info(f"Enriched data: {enriched_data}")
            return enriched_data
        except Exception as e:
            logger.error(f"Error enriching data: {str(e)}")
            raise

    def take_action(self, alert):
        try:
            # Define the action to be taken
            logger.info("Action taken for new alert")
        except Exception as e:
            logger.error(f"Error taking action: {str(e)}")
            raise
```
### 2. Register the New Handler

2.1. Update src/handler_factory.py to include the new handler:

```python
# src/handler_factory.py

from src.handlers.kube_pod_crash_looping import KubePodCrashLoopingHandler
from src.handlers.new_alert_handler import NewAlertHandler

class AlertHandlerFactory:
    @staticmethod
    def get_handler(alert):
        alertname = alert.get("labels", {}).get("alertname")
        if alertname == "KubePodCrashLooping":
            return KubePodCrashLoopingHandler()
        elif alertname == "NewAlertName":
            return NewAlertHandler()
        # Add more handlers for different alert types here
        return None
```
