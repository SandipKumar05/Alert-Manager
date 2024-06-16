import requests

from src.config import PROMETHEUS_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)


def fetch_metric(query):

    api_url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": query}

    response = requests.get(api_url, params=params)
    response_json = response.json()

    if response.status_code == 200:
        try:
            result = response_json["data"]["result"]
            return result
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error parsing Prometheus response: {e}")
            return None
    else:
        logger.error(f"Failed to fetch metric from Prometheus: {response.status_code}")
        return None


def fetch_cpu_usage(namespace, pod, container):
    cpu_query = f'rate(container_cpu_usage_seconds_total{{namespace="{namespace}",pod="{pod}",container="{container}"}}[5m])'
    cpu_result = fetch_metric(cpu_query)

    # taking first one if we got multipe entry
    for result in cpu_result:
        logger.info(f"Pod: {result['metric']['pod']}, Value: {result['value'][1]}")
        # return result in micro cpu
        return float(result["value"][1]) / 1000


def fetch_memory_usage(namespace, pod, container):
    memory_query = f'container_memory_usage_bytes{{namespace="{namespace}",pod="{pod}",container="{container}"}}'
    memory_results = fetch_metric(memory_query)

    # taking first one if we got multipe entry
    for result in memory_results:
        logger.info(f"Pod: {result['metric']['pod']}, Value: {result['value'][1]}")
        # return result in MB
        return float(result["value"][1]) / (1024 * 1024)
