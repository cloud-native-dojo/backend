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
    name: str

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


    return {"name": callback}

@app.get("/pods/")
def get_pod():
    return {"output": k8s.get_pod()}

@app.post("/services/")
def create_service(service: Service):
    callback = k8s.change_port(name)
    return {"result": callback}

@app.get("/ports_suggest/")
def get_unused_port():
    ports = k8s.get_used_port()
    return {"sugessted_port":ports}

@app.delete("/pods/{name}")
def delete_pod():
    callback = k8s.delete_pod(name)
    return {"deleted": callback}

@app.delete("/services/{name}")
def delete_pod(name: str):
    return {"status": "test"}