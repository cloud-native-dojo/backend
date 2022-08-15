import time

import subprocess, sys

def make_pod():
    cp = subprocess.run(['C:/Program Files/helm/helm','--set', 'service.type=NodePort', 'install', 'bitnami/wordpress', '--generate-name'])
    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)
    
    out = get_pod()
    return out

def get_pod():
    cp = subprocess.run(['kubectl', 'get', 'svc', '--no-headers', '-o', 'custom-columns=\"NAME:.metadata.name,IP:.spec.clusterIP,PORT:.spec.ports[*].targetPort\"'], encoding='utf-8', stdout=subprocess.PIPE)
    return cp.stdout.split('\n')