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


def create_vm():
    server_url = "http://89.248.207.43/compute/v2.1/servers"
    params = {
        "server": {
            "name": "Standart",
            "networks": [
                {
                    "port": create_port()['port']['id']
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
    return resp.json()

def delete_port(port_id):
    port_url = f"http://89.248.207.43:9696/v2.0/ports/{port_id}"
    headers = {
        "Content-Type":"application/json",
        "X-Auth-Token": get_auth_token()["X-Auth-Token"]
    }
    resp = requests.delete(url=port_url, headers=headers)
    return resp.json()

def delete_vm():
    ...

def get_vm():
    server_url="http://89.248.207.43/compute/v2.1/servers"
    headers = {
        "Content-Type":"application/json",
         "X-Auth-Token": get_auth_token()["X-Auth-Token"]

    }
    resp = requests.get(server_url, headers=headers)
    return resp.json()