import time

from kubernetes import client, config

from src.utils.logger import logger

config.load_kube_config()


def delete_pod(pod_name, namespace):

    core_v1 = client.CoreV1Api()
    pod = core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)

    # Restart the pod by deleting and recreating it
    core_v1.delete_namespaced_pod(
        name=pod_name, namespace=namespace, body=client.V1DeleteOptions()
    )
    logger.info(
        f"Pod {pod_name} in namespace {namespace} deleted. Waiting for it to be recreated..."
    )

    # # Wait for the pod to be recreated
    # import time
    # time.sleep(5)  # Adjust this delay as needed based on your pod startup time

    # # Optional: Check if the pod is running again
    # pod = core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    # if pod.status.phase == "Running":
    #     print(f"Pod {pod_name} successfully restarted.")
    # else:
    #     print(f"Pod {pod_name} restart failed or is not running.")
