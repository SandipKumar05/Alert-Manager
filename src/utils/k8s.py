from kubernetes import client, config

from src.utils.logger import get_logger

logger = get_logger(__name__)
config.load_incluster_config()


def delete_pod(pod_name, namespace):

    core_v1 = client.CoreV1Api()
    pod = core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)

    core_v1.delete_namespaced_pod(
        name=pod_name, namespace=namespace, body=client.V1DeleteOptions()
    )
    logger.info(f"Pod {pod_name} in namespace {namespace} deleted.")
