import time

import subprocess, sys

def make_pod():
    cp = subprocess.run(['C:/Program Files/helm/helm','--set', 'service.type=NodePort,persistence.storageClass=longhorn', 'install', 'bitnami/wordpress', '--generate-name'], encoding='utf-8', stdout=subprocess.PIPE)
    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)
    return cp.stdout.split('\n')[0].replace('NAME: ', '')

def get_pod():
    cp = subprocess.run(['helm', 'list', '--short'], encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout.split('\n')

def delete_pod(pod_name):
    cp = subprocess.run(['helm', 'uninstall', '--purge'], encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout