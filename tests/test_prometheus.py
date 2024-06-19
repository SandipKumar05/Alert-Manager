import pytest
from unittest.mock import patch, MagicMock
from src.utils.prometheus import fetch_cpu_usage, fetch_memory_usage

# Mock response data for fetch_metric function
mock_metric_response = [
            {
                "metric": {"pod": "test-pod"},
                "value": [1596479123.573, "100"] # mock value for cpu or memory
            }
        ]

@pytest.fixture
def mock_fetch_metric():
    with patch("src.utils.prometheus.fetch_metric") as mock_fetch_metric:
        # configure the mock to return the mock_metrics_response
        mock_fetch_metric.return_value = mock_metric_response
        yield mock_fetch_metric

def test_fetch_cpu_usage(mock_fetch_metric):
    namespace = "default"
    pod = "test-pod"
    container = "test-container"

    # Call the function under test
    cpu_usage = fetch_cpu_usage(namespace, pod, container)

    # Assertions
    assert cpu_usage == float(mock_metric_response[0]["value"][1]) / 1000
    mock_fetch_metric.assert_called_once_with(
        f'rate(container_cpu_usage_seconds_total{{namespace="{namespace}",pod="{pod}",container="{container}"}}[5m])'
    )

def test_fetch_memory_usage(mock_fetch_metric):
    namespace = "default"
    pod = "test-pod"
    container = "test-container"

    memory_usage = fetch_memory_usage(namespace, pod, container)

    assert memory_usage == float(mock_metric_response[0]["value"][1]) / (1024*1024)
    mock_fetch_metric.assert_called_once_with(
        f'container_memory_usage_bytes{{namespace="{namespace}",pod="{pod}",container="{container}"}}'
    )
