import time

import subprocess
import sys
import shlex
from random import randint


def make_pod():
    cp = subprocess.run(['helm', '--set', 'service.type=NodePort,persistence.storageClass=longhorn',
                        'install', 'bitnami/wordpress', '--generate-name'], encoding='utf-8', stdout=subprocess.PIPE)
    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)
    return cp.stdout.split('\n')[0].replace('NAME: ', '')


def get_pod():
    cp = subprocess.run(['helm', 'list', '--short'], encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout[:-1].split('\n')


def delete_pod(name):
    cp = subprocess.run(['helm', 'uninstall', name],
                        encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout


def get_used_port():
    cp = subprocess.run(['kubectl', 'get', 'svc', '--all-namespaces', '-o',
                        'go-template=\'{{range .items}}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{"\\n"}}{{end}}{{end}}{{end}}\''], encoding='utf-8', stdout=subprocess.PIPE)
    ports = cp.stdout[1:-2].split('\n')
    print(f"return:{ports}")
    unusedport = []
    while(len(unusedport) < 4):
        num = randint(30000, 32768)
        if num not in ports and num not in unusedport:
            unusedport.append(num)
    print(unusedport)
    return unusedport


def update_port(name, port):
    cp = subprocess.run(['kubectl', 'patch', 'service', name, '--type=\'json\'',
                        '-p=\'[{"op": "replace", "path": "/spec/ports/0/nodePort", "value": {}}]\''.format(port)], encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout
