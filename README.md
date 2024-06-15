# Alert Manager

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
### 3. Test the New Handler

3.1. Add tests for the new handler in tests/test_handlers.py:

```python
# tests/test_handlers.py

from src.handlers.new_alert_handler import NewAlertHandler

def test_new_alert_enrich_data():
    handler = NewAlertHandler()
    alert = {"annotations": {"description": "test", "summary": "test"}}
    enriched_data = handler.enrich_data(alert)
    assert "additional_info" in enriched_data

def test_new_alert_take_action(mocker):
    handler = NewAlertHandler()
    mocker.patch("requests.post")
    enriched_data = {"annotations": {"description": "test", "summary": "test"}}
    handler.take_action(enriched_data)
    requests.post.assert_called_once()

```
### 4. Runs the test
```bash
pytest
```
