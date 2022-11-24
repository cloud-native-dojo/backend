import subprocess
import json


def pod_status():
    sp = subprocess.run(
        ["kubectl", "-n", "planetes", "get", "pod", "-o", "json"],
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    status = json.loads(sp.stdout.replace("\n", ""))
    result = {}

    for s in status["items"]:
        try:
            pod_name = s["metadata"]["name"]
            # print(pod_name)

            containers_status = []
            for container in s["status"]["containerStatuses"]:
                # print(container['ready'])
                containers_status.append(container["ready"])

            result[pod_name] = containers_status
            # print(json.dumps({"name": pod_name, "body": pod_status}))
        except Exception:
            continue

    return result


# x = pod_status()
# print(x)

# print(status['items'][0]['metadata']['name'])
# print(status['items'][0]['status']['containerStatuses'][0]['ready'])
