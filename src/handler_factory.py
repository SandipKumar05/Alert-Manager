from src.handlers.kube_pod_crash_looping import KubePodCrashLooping


class AlertHandlerFactory:
    @staticmethod
    def get_handler(alert):
        alertname = alert.get("lables", {}).get("alertname")

        if alertname == "KubePdCrashLooping":
            return KubePodCrashLooping()

        # add more handlers for different types here
        return None
