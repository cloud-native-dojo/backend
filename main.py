from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from kubernetes import client, config
import k8s

app = FastAPI()

class Pod(BaseModel):
    containers: Dict[str, int]

class Service(BaseModel):
    port: int
    pod_name: str

@app.get("/")
def read_root():
    return {"status": "test"}


@app.post("/pods/")
def create_pod(pod: Pod):
    print(pod)
    for container in pod.containers.items():
        print(container)
        if container[0] == "wordpress":
            callback = k8s.make_pod()


    return {"pod_name": callback}

@app.get("/pods/")
def get_pod():
    return {"output": k8s.get_pod()}

@app.post("/services/")
def create_service(service: Service):
    return {"service_name": "test_name"}

@app.delete("/pods/{pod_name}")
def delete_pod():
    callback = k8s.delete_pod(pod_name)
    return {"deleteed": callback}

@app.delete("/services/{service_name}")
def delete_pod(service_name: str):
    return {"status": "test"}