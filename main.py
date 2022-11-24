from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from random import randint
import k8s

app = FastAPI()

ports = k8s.get_used_port()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pod(BaseModel):
    containers: Dict[str, int]
    name: str


class Service(BaseModel):
    port: int
    name: str


class Save(BaseModel):
    island: Dict[str, str]
    ship: Dict[str, str]


class Shipname(BaseModel):
    name: str


@app.get("/")
def read_root():
    return {"status": "test"}


@app.post("/pods/")
def create_pod(pod: Pod):
    print(pod)
    for container in pod.containers.items():
        print(container)
        print("data:" + pod.name)
        if pod.name == "":
            callback = k8s.makepodwithname("ship-" + str(randint(10000, 99999)),container[0])
        else:
            callback = k8s.makepodwithname(pod.name,container[0])

    return {"name": callback}


@app.get("/pods/")
def get_pod():
    return {"pods": k8s.get_pod()}

@app.get("/{shipname}/pass/")
def get_pass(shipname: str):
    callback = k8s.get_pass(shipname)
    return {"pass": callback}

@app.post("/services/")
def create_service(service: Service):
    print(service.port)
    callback = k8s.update_port(service.name, service.port)
    return {"result": callback}


@app.get("/generate_ports/")
def get_unused_port():
    ports = k8s.get_used_port()
    return {"sugessted_port": ports}


@app.get("/ports_suggest/")
def get_unused_port():
    return {"sugessted_port": ports}


@app.delete("/pods/")
def delete_pod(shipname: Shipname):
    callback = k8s.delete_pod(shipname.name)
    return {"deleted": callback}


@app.delete("/services/{name}")
def delete_pod(name: str):

    return {"status": "test"}


save_data = {"island": {}, "ship": {}}


@app.post("/save/")
def post_save(save: Save):
    global save_data
    save_data = save
    return {"data": save_data}


@app.get("/save/")
def get_save():
    return {"data": save_data}


@app.get("/pods/status/")
def pod_status():
    return {"data": k8s.get_status(k8s.get_pod())}
