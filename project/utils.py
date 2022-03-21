import requests
import os


COMPUTE_URL = os.environ.get('COMPUTE_URL')
PORT_URL = os.environ.get('PORT_URL')


def get_cloud_headers_auth() -> dict:
    """Get request headers for auth in openstack

    :return: headers for auth in openstack
    :rtype: dict
    """
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


def create_cloud_vm(name: str) -> dict:
    """Create vm in openstack by name

    :param name: name for vm
    :type name: str
    :return: dict with vm parameters
    :rtype: dict
    """
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
    if resp.status_code == 403:
        return {
            'code': '403',
            'message': 'Cant create vm in cloud'
        }
    cloud_id = resp.json()["server"]["id"]
    return {
        "name": name,
        "cloud_port_id": cloud_port_id,
        "cloud_id": cloud_id
    }
    

def create_local_vm(vm_params: dict, is_preemptible: bool) -> None:
    """Create row in local db table that describe vm from openstack

    :param vm_params: dict with dm parameters, like name etc.
    :type vm_params: dict
    :param is_preemptible: bool value, that describe vm preemptible or standart
    :type is_preemptible: bool
    """
    from app import db, VMInstanse

    vm = VMInstanse(
        name=vm_params["name"],
        is_preemptible=is_preemptible,
        cloud_id=vm_params["cloud_id"],
        cloud_port_id=vm_params["cloud_port_id"],
    )
    db.session.add(vm)
    db.session.commit()


def create_vm(is_preemptible: bool = False) -> dict:
    """Create standart or preemptible vm in openstack

    :param is_preemptible: bool value, that describe 
    vm preemptible or standart, defaults to False
    :type is_preemptible: bool, optional
    :return: dict with code and message about succesfully result
    :rtype: dcit
    """
    from app import db, VMInstanse

    instanse = db.session.query(VMInstanse).first()
    if instanse:
        if instanse.is_preemptible:
            if not is_preemptible:
                del_result = delete_vm(instanse.cloud_id)
                if del_result.get('code') == '403':
                    return del_result
                vm_params = create_cloud_vm(name="standart")
                if vm_params.get('code'):
                    return {
                        'code':'404',
                        'message:': "Cant create vm in cloud"
                    }
                create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
                result = {
                    'code':'201',
                    'message:': f"Standart vm {vm_params['cloud_id']} was created succesfully instead of the preemptible vm"
                }
            else:
                result = {
                    'code':'403',
                    'message:': "It is impossible to create a preemptible vm because one has already been created"
                }
        else:
            result = {
                'code':'403',
                'message:': "It is impossible to create a vm because the created machine is non-preemptable"
            }
    else:
        if not is_preemptible:
            vm_params = create_cloud_vm(name="standart")
            if vm_params.get('code'):
                return {
                    'code':'404',
                    'message:': "Cant create vm in cloud"
                }
            create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = {
                'code':'201',
                'message:': f"Standart vm {vm_params['cloud_id']} was created succesfully"
            }
        else:
            vm_params = create_cloud_vm(name="preemptible")
            if vm_params.get('code'):
                return {
                    'code':'404',
                    'message:': "Cant create vm in cloud"
                }
            create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = {
                'code':'201',
                'message:': f"Preemptible vm {vm_params['cloud_id']} was created succesfully"
            }
    return result


def delete_vm(cloud_vm_id: str) -> dict:
    """Delete vm in openstack and local db

    :param cloud_vm_id: id vm from openstack
    :type cloud_vm_id: str
    :return: dict with code and message about succesfully result
    :rtype: dict
    """
    from app import db, VMInstanse

    instanse = (
        db.session.query(VMInstanse).filter(VMInstanse.cloud_id == cloud_vm_id).first()
    )
    if instanse is None:
        return {
            'code':'403',
            'message:':  f"vm {cloud_vm_id} does not exist"
        }
    if not delete_cloud_vm(cloud_vm_id=instanse.cloud_id):
        return {
            'code':'403',
            'message:':  f"cant delete vm {cloud_vm_id} in cloud"
        }
    if not delete_cloud_port(cloud_port_id=instanse.cloud_port_id):
        return {
            'code':'403',
            'message:':  f"cant delete port on vm {cloud_vm_id} in cloud"
        }
    db.session.delete(instanse)
    db.session.commit()
    return {
        'code':'204',
        'message:': f"vm {cloud_vm_id} was deleted succesfully"
    }


def delete_cloud_vm(cloud_vm_id: str) -> bool:
    """Delete vm in openstack

    :param cloud_vm_id: id vm from openstack
    :type cloud_vm_id: str
    :return: success result or not
    :rtype: bool
    """
    server_url = f"{COMPUTE_URL}/{cloud_vm_id}"
    response = requests.delete(url=server_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False


def delete_cloud_port(cloud_port_id: str) -> bool:
    """Delete port in openstack

    :param cloud_port_id: id port from openstack
    :type cloud_port_id: str
    :return: success result or not
    :rtype: bool
    """
    port_url = f"{PORT_URL}/{cloud_port_id}"
    response = requests.delete(url=port_url, headers=get_cloud_headers_auth())
    if response.status_code == 204:
        return True
    return False


def get_cloud_vm() -> dict:
    """Get info about openstack virtual machines

    :return: json with info about vm
    :rtype: dict
    """
    server_url = COMPUTE_URL
    resp = requests.get(server_url, headers=get_cloud_headers_auth())
    return resp.json()


def create_cloud_port() -> dict:
    """Creat network port in openstack

    :return: json with info about port
    :rtype: dict
    """
    ports_url = PORT_URL
    params = {
        "port": {
            "network_id": os.environ.get('NETWORK_ID'),
            "fixed_ips": [{"subnet_id": os.environ.get('SUBNET_ID')}],
        }
    }
    resp = requests.post(url=ports_url, json=params, headers=get_cloud_headers_auth())
    return resp.json()
