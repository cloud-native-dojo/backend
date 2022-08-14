from kubernetes import client, config, watch
import yaml

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

with open("pod.yaml", "r",encoding="utf-8_sig") as f:
    pod = yaml.safe_load(f)
    k8s_apps_v1 = client.CoreV1Api()
    resp = k8s_apps_v1.create_namespaced_pod(body=pod, namespace="sample")
    print("pod created. status='%s'" % resp.metadata.name)