import time

import subprocess
import sys
import shlex
import pod_status
from random import randint


def makepodwithname(name,soft_name):
    soft = "bitnami/" + soft_name
    if soft_name == "mediawiki":
        cp = subprocess.run(
            [
                "helm",
                "install",
                "--set",
                "service.type=ClusterIP,persistence.storageClass=longhorn,resources.requests.cpu=null,persistence.size=2Gi,mariadb.primary.persistence.size=2Gi",
                "--namespace=planetes",
                name,
                "bitnami/" + soft_name,
                "-f",
                "values.yml"
            ],
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
    else:
        cp = subprocess.run(
            [
                "helm",
                "install",
                "--set",
                "service.type=ClusterIP,persistence.storageClass=longhorn,resources.requests.cpu=null,persistence.size=2Gi,mariadb.primary.persistence.size=2Gi",
                "--namespace=planetes",
                name,
                "bitnami/" + soft_name,
            ],
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
    if cp.returncode != 0:
        print("ls failed.", file=sys.stderr)
        sys.exit(1)
    return cp.stdout.split("\n")[0].replace("NAME: ", "")


def get_pod():
    cp = subprocess.run(
        ["helm", "list", "-n", "planetes", "--short"],
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    return cp.stdout[:-1].split("\n")

def get_pass(name):
    cp = subprocess.run(
        "kubectl get secret -n planetes " + name + "-wordpress -o jsonpath=\"{.data.wordpress-password}\" | base64 --decode",
        encoding="utf-8",
        stdout=subprocess.PIPE,
        shell=True,
    )
    return cp.stdout

def delete_pod(name):
    try:
        cp = subprocess.run(
            ["helm", "delete", "--namespace", "planetes", name],
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
    except:
        pass
    try:
        pvdelete1 = subprocess.run(
            'kubectl get pvc -n planetes --no-headers -o custom-columns=":metadata.name"',
            capture_output=True,
            text=True,
            shell=True,
        )
        pvdelete2 = subprocess.run(
            ["grep", "data-" + name],
            capture_output=True,
            text=True,
            input=pvdelete1.stdout,
        )
        pvdelete3 = subprocess.run(
            ["tr", "-s", '"\n"', '" "'],
            capture_output=True,
            text=True,
            input=pvdelete2.stdout,
        )
        pvdelete4 = subprocess.run(
            ["kubectl", "delete", "pvc", "-n", "planetes", pvdelete3.stdout[:-1]]
        )
    except:
        pass
    # return cp.stdout


def get_used_port():
    cp = subprocess.run(
        [
            "kubectl",
            "get",
            "svc",
            "--all-namespaces",
            "-o",
            "go-template='{{range .items}}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{\"\\n\"}}{{end}}{{end}}{{end}}'",
        ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    ports = cp.stdout[1:-2].split("\n")
    print(f"return:{ports}")
    unusedport = []
    while len(unusedport) < 4:
        num = randint(30000, 32768)
        if num not in ports and num not in unusedport:
            unusedport.append(num)
    print(unusedport)
    return unusedport


def update_port(name: str, port: int):
    print(port)
    target1 = subprocess.run(
        'kubectl get service -n planetes --no-headers -o custom-columns=":metadata.name"',
        capture_output=True,
        text=True,
        shell=True,
    )
    target2 = subprocess.run(
        ["grep", name + "-"],
        capture_output=True,
        text=True,
        input=target1.stdout,
    )
    target3 = subprocess.run(
        ["grep", "-v", "mariadb"],
        capture_output=True,
        text=True,
        input=target2.stdout,
    )
    target_name = target3.stdout[:-1]

    if port == -1:
        print("reset_port")
        cp1 = subprocess.run(
            "kubectl patch service "
            + target_name
            + ' -n planetes -p \'{"spec":{"type": "ClusterIP"}}\'',
            shell=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
    else:
        port_num = str(port)
        cp2 = subprocess.run(
            "kubectl patch service "
            + target_name
            + ' -n planetes --type=json -p=\'[{"op": "replace", "path": "/spec/type", "value": "NodePort"}]\'',
            shell=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
        cp1 = subprocess.run(
            "kubectl patch service "
            + target_name
            + ' -n planetes --type=json -p=\'[{"op": "replace", "path": "/spec/ports/0/nodePort", "value":'
            + port_num
            + "}]'",
            shell=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
    return cp1.stdout


def get_status(names: list):
    all_status = pod_status.pod_status()
    result = []
    for name in names:
        status = True
        flag = False
        for i in all_status.items():
            if i[0].startswith(name):
                flag = True
                if not all(i[1]):
                    status = False
        if flag == False:
            status = False
        result.append(status)
    return result
