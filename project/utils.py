import requests
import os
from project.message import (
    get_success_create_st_vm_mes,
    get_success_create_pr_vm_mes,
    get_success_create_st_vm_af_pr_mes,
    get_err_vm_404_mes,
    get_err_vm_exist_mes,
    get_err_vm_not_pr_mes,
    get_success_del_vm_mes,
    get_err_del_vm_mes,
    get_err_del_cloud_vm_mes,
    get_err_del_cloud_port_mes
)

COMPUTE_URL = os.environ.get('COMPUTE_URL')
PORT_URL = os.environ.get('PORT_URL')


def get_auth_params() -> dict:
    """Get necessary params dict with secret values

    :return: dict with secret values
    :rtype: dict
    """
    return {
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


def get_cloud_headers_auth() -> dict:
    """Get request headers for auth in openstack

    :return: headers for auth in openstack
    :rtype: dict
    """
    aut_url = os.environ.get('AUTH_URL')

    response = requests.post(url=aut_url, json=get_auth_params())
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
        return get_err_vm_404_mes()

    return {
        "name": name,
        "cloud_port_id": cloud_port_id,
        "cloud_id": resp.json()["server"]["id"]
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
                    return get_err_vm_404_mes()
                create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
                result = get_success_create_st_vm_af_pr_mes(vm_params['cloud_id'])
            else:
                result = get_err_vm_exist_mes()
        else:
            result = get_err_vm_not_pr_mes()
    else:
        if not is_preemptible:
            vm_params = create_cloud_vm(name="standart")
            if vm_params.get('code'):
                return get_err_vm_404_mes()
            create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = get_success_create_st_vm_mes(vm_params['cloud_id'])
        else:
            vm_params = create_cloud_vm(name="preemptible")
            if vm_params.get('code'):
                return get_err_vm_404_mes()
            create_local_vm(vm_params=vm_params, is_preemptible=is_preemptible)
            result = get_success_create_pr_vm_mes(vm_params['cloud_id'])
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
        return get_err_del_vm_mes(cloud_vm_id)

    if not delete_cloud_vm(cloud_vm_id=instanse.cloud_id):
        return get_err_del_cloud_vm_mes(cloud_vm_id)

    if not delete_cloud_port(cloud_port_id=instanse.cloud_port_id):
        return get_err_del_cloud_port_mes(cloud_vm_id)

    db.session.delete(instanse)
    db.session.commit()
    return get_success_del_vm_mes(cloud_vm_id)


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
    """Create network port in openstack

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
