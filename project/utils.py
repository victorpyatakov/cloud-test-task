import requests
import os


COMPUTE_URL = os.environ.get('COMPUTE_URL')
PORT_URL = os.environ.get('PORT_URL')


def get_cloud_headers_auth() -> dict:
    aut_url = os.environ.get('AUTH_URL')

    params = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": os.environ.get('OS_USERNAME'),
                        "domain": {"name": os.environ.get('OS_USER_DOMAIN_NAME')},
                        "password": os.environ.get('OS_PASSWORD'),
                    }
                },
            },
            "scope": {"project": {"name": os.environ.get('OS_PROJECT_NAME'),
                      "domain": {"name": os.environ.get('OS_PROJECT_DOMAIN_NAME')}}},
        }
    }

    response = requests.post(url=aut_url, json=params)
    return {
        "Content-Type": "application/json",
        "X-Auth-Token": response.headers["X-Subject-Token"],
    }


def create_cloud_vm(name):
    server_url = COMPUTE_URL
    cloud_port_id = create_cloud_port()["port"]["id"]
    params = {
        "server": {
            "name": name,
            "networks": [{"port": cloud_port_id}],
            "imageRef": os.environ.get('imageRef'),
            "flavorRef": os.environ.get('flavorRef'),
        }
    }
    resp = requests.post(url=server_url, json=params, headers=get_cloud_headers_auth())
    cloud_id = resp.json()["server"]["id"]
    return {"name": name, "cloud_port_id": cloud_port_id, "cloud_id": cloud_id}


def create_bd_vm(vm_params: dict, is_preemptible: bool):
    from app import db, VMInstanse

    vm = VMInstanse(
        name=vm_params["name"],
        is_preemptible=is_preemptible,
        cloud_id=vm_params["cloud_id"],
        cloud_port_id=vm_params["cloud_port_id"],
    )
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
                result = "cоздана стадарт вм вместо вытесняемой"
            else:
                result = "нельзя создать вытесняемую вм так как уже создана такая"
        else:
            result = "нельзя создать вм так как созданая машина является не вытесянемой"
    else:
        if not is_preemptible:
            vm_params = create_cloud_vm(name="standart")
            create_bd_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = "cоздана стадарт вм"
        else:
            vm_params = create_cloud_vm(name="preemptible")
            create_bd_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = "cоздана вытесняемая вм"
    return result


def delete_vm(server_id):
    from app import db, VMInstanse

    instanse = (
        db.session.query(VMInstanse).filter(VMInstanse.cloud_id == server_id).first()
    )
    delete_cloud_vm(instanse_id=instanse.cloud_id)
    delete_cloud_port(port_id=instanse.cloud_port_id)
    db.session.delete(instanse)
    db.session.commit()
    return f"vm {server_id} was deleted succesfully"


def delete_cloud_vm(instanse_id):
    server_url = f"{COMPUTE_URL}/{instanse_id}"
    response = requests.delete(url=server_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False


def delete_cloud_port(port_id):
    port_url = f"{PORT_URL}/{port_id}"
    response = requests.delete(url=port_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False


def get_cloud_vm():
    server_url = COMPUTE_URL
    resp = requests.get(server_url, headers=get_cloud_headers_auth())
    return resp.json()


def create_cloud_port():
    ports_url = PORT_URL
    params = {
        "port": {
            "network_id": os.environ.get('NETWORK_ID'),
            "fixed_ips": [{"subnet_id": os.environ.get('SUBNET_ID')}],
        }
    }
    resp = requests.post(url=ports_url, json=params, headers=get_cloud_headers_auth())
    return resp.json()
