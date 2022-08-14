from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from kubernetes import client, config

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
    for container in pod:
         
    return {"pod_name": pod}

@app.post("/services/")
def create_service(service: Service):
    return {"service_name": "test_name"}

@app.delete("/pods/{pod_name}")
def delete_pod(pod_name: str):
    return {"status": "test"}

@app.delete("/services/{service_name}")
def delete_pod(service_name: str):
    return {"status": "test"}