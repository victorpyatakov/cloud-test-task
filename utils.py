from glob import escape
import requests


def get_auth_token():
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

    resp = requests.post(url=aut_url, json=params)
    token = resp.headers["X-Subject-Token"]
    return {"X-Auth-Token": token}

def create_port():
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
    headers = {
        "Content-Type":"application/json",
        "X-Auth-Token": get_auth_token()["X-Auth-Token"]
    }
    resp = requests.post(url=ports_url, json=params, headers=headers)
    return resp.json()


def create_vm(is_preemptible: bool = False):
    from app import db, VMInstanse
    server_url = "http://89.248.207.43/compute/v2.1/servers"
    # проверяем в бд есть ли говно
    instanse = db.session.query(VMInstanse).first()
    is_preemptible=False
    # если есть
    if instanse:
        if instanse.is_preemptible:
            if not is_preemptible:
                delete_vm(instanse.cloud_id)
                delete_port(instanse.cloud_port_id)
                db.session.delete(instanse)
                # создаем в облаке
                #
                name = "standart"
                cloud_port_id = create_port()['port']['id']
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
                headers = {
                    "Content-Type":"application/json",
                    "X-Auth-Token": get_auth_token()["X-Auth-Token"]
                }
                resp = requests.post(url=server_url, json=params, headers=headers)
                cloud_id = resp.json()["server"]["id"]
                is_preemptible=False
                # создаем в бд
                vm = VMInstanse(name=name, is_preemptible=is_preemptible,cloud_id=cloud_id,cloud_port_id=cloud_port_id)
                db.session.add(vm)
                db.session.commit()
                result = "создана стадарт вм"
            else:
                result = "нельзя создать вытесняемую вм так как уже создана такая"
        else:
            result = "нельзя создать вм так как созданая машина является не вытесянемой"
    else:
        if not is_preemptible:
            name = "standart"
            cloud_port_id = create_port()['port']['id']
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
            headers = {
                "Content-Type":"application/json",
                "X-Auth-Token": get_auth_token()["X-Auth-Token"]
            }
            resp = requests.post(url=server_url, json=params, headers=headers)
            cloud_id = resp.json()["server"]["id"]
            is_preemptible=False
            # создаем в бд
            vm = VMInstanse(name=name, is_preemptible=is_preemptible,cloud_id=cloud_id,cloud_port_id=cloud_port_id)
            db.session.add(vm)
            db.session.commit()
            result = "создана стадарт вм"
        else:
            name = "preemptible"
            cloud_port_id = create_port()['port']['id']
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
            headers = {
                "Content-Type":"application/json",
                "X-Auth-Token": get_auth_token()["X-Auth-Token"]
            }
            resp = requests.post(url=server_url, json=params, headers=headers)
            cloud_id = resp.json()["server"]["id"]
            is_preemptible=True
            # создаем в бд
            vm = VMInstanse(name=name, is_preemptible=is_preemptible,cloud_id=cloud_id,cloud_port_id=cloud_port_id)
            db.session.add(vm)
            db.session.commit()
            result = "создана вытесняемая вм"
    
    return result

def delete_port(port_id):
    port_url = f"http://89.248.207.43:9696/v2.0/ports/{port_id}"
    headers = {
        "Content-Type":"application/json",
        "X-Auth-Token": get_auth_token()["X-Auth-Token"]
    }
    resp = requests.delete(url=port_url, headers=headers)
    return True

def delete_vm(server_id):
    server_url=f"http://89.248.207.43/compute/v2.1/servers/{server_id}"
    headers = {
        "Content-Type":"application/json",
        "X-Auth-Token": get_auth_token()["X-Auth-Token"]
    }
    resp = requests.delete(url=server_url, headers=headers)
    return True

def get_vm():
    server_url="http://89.248.207.43/compute/v2.1/servers"
    headers = {
        "Content-Type":"application/json",
         "X-Auth-Token": get_auth_token()["X-Auth-Token"]

    }
    resp = requests.get(server_url, headers=headers)
    return resp.json()