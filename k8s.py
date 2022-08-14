import time

import subprocess, sys

def main():
    cp = subprocess.run(['C:/Program Files/helm/helm','--set', 'service.type=NodePort', 'install', 'bitnami/wordpress', '--generate-name'])
    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)
    
    cp = subprocess.run(['kubectl', 'get', 'svc'], encoding='utf-8', stdout=subprocess.PIPE)
    print(f'{cp.stdout}')


if __name__ == '__main__':
    main()