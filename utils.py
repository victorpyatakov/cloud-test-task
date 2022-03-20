import requests


def get_cloud_headers_auth() -> dict:
    aut_url = "http://89.248.207.43/identity/v3/auth/tokens"

    params = { "auth": 
                { 
            "identity": 
                { 
                    "methods": ["password"], 
                    "password": 
                        { "user": 
                            { 
                                "name": "demo",  
                                "domain": 
                                    {   
                                        "name": "Default" 
                                    }, 
                                "password": "secret" 
                            } 
                        } 
                    }, 
            "scope": 
                { 
                    "project": 
                        { 
                            "name": "demo", 
                            "domain": 
                                { 
                                    "name": "Default"
                                }
                        }
                }
        }
    }

    response = requests.post(url=aut_url, json=params)
    return  {
        "Content-Type":"application/json",
        "X-Auth-Token": response.headers["X-Subject-Token"]
    }


def create_cloud_vm(name):
    server_url = "http://89.248.207.43/compute/v2.1/servers"
    cloud_port_id = create_cloud_port()['port']['id']
    params = {
        "server": {
            "name": name,
            "networks": [
                {
                    "port": cloud_port_id
                }
            ],
            "imageRef": "713f7ee3-c787-49ea-b68d-7f3c86a09cf2",
            "flavorRef": "c1" 
        }
    }
    resp = requests.post(url=server_url, json=params, headers=get_cloud_headers_auth())
    cloud_id = resp.json()["server"]["id"]
    return {
        "name": name,
        "cloud_port_id": cloud_port_id,
        "cloud_id": cloud_id
    }


def create_bd_vm(vm_params:dict, is_preemptible:bool):
    from app import db, VMInstanse
    vm = VMInstanse(name=vm_params["name"], 
                    is_preemptible=is_preemptible,
                    cloud_id=vm_params["cloud_id"],
                    cloud_port_id=vm_params["cloud_port_id"])
    db.session.add(vm)
    db.session.commit()


def create_vm(is_preemptible: bool = False):
    from app import db, VMInstanse
    instanse = db.session.query(VMInstanse).first()
    if instanse:
        if instanse.is_preemptible:
            if not is_preemptible:
                delete_vm(instanse.cloud_id)
                vm_params = create_cloud_vm(name="standart")
                create_bd_vm(vm_params=vm_params, is_preemptible=is_preemptible)
                result = "создана стадарт вм вместо вытесняемой"
            else:
                result = "нельзя создать вытесняемую вм так как уже создана такая"
        else:
            result = "нельзя создать вм так как созданая машина является не вытесянемой"
    else:
        if not is_preemptible:
            vm_params = create_cloud_vm(name="standart")
            create_bd_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = "создана стадарт вм"
        else:
            vm_params = create_cloud_vm(name="preemptible")
            create_bd_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = "создана вытесняемая вм"
    return result


def delete_vm(server_id):
    from app import db, VMInstanse
    instanse = db.session.query(VMInstanse).filter(VMInstanse.cloud_id == server_id).first()
    delete_cloud_vm(instanse_id=instanse.cloud_id)
    delete_cloud_port(port_id=instanse.cloud_port_id)
    db.session.delete(instanse)
    db.session.commit()
    return f'vm {server_id} was deleted succesfully'

def delete_cloud_vm(instanse_id):
    server_url=f"http://89.248.207.43/compute/v2.1/servers/{instanse_id}"
    response = requests.delete(url=server_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False

def delete_cloud_port(port_id):
    port_url = f"http://89.248.207.43:9696/v2.0/ports/{port_id}"
    response = requests.delete(url=port_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False

def get_cloud_vm():
    server_url="http://89.248.207.43/compute/v2.1/servers"
    resp = requests.get(server_url, headers=get_cloud_headers_auth())
    return resp.json()

def create_cloud_port():
    ports_url = "http://89.248.207.43:9696/v2.0/ports"
    params = {
        "port": {
            "network_id": "0c81a9ab-7549-4c47-8875-58f6d1059fba",
            "fixed_ips": [
                {
                    "subnet_id": "01144954-7fea-4b8d-bd8b-c36575c872ed"
                }
            ]
        }
    }
    resp = requests.post(url=ports_url, json=params, headers=get_cloud_headers_auth())
    return resp.json()