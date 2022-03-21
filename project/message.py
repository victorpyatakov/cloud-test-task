def get_success_create_st_vm_mes(cloud_id: str) -> dict:
    return {
        'code': '201',
        'message:': f"Standart vm {cloud_id} was created succesfully"
    }


def get_success_create_pr_vm_mes(cloud_id: str) -> dict:
    return {
        'code': '201',
        'message:': (
            f"Preemptible vm {cloud_id}"
            " was created succesfully"
        )
    }


def get_success_create_st_vm_af_pr_mes(cloud_id: str) -> dict:
    return {
        'code': '201',
        'message:': (
            f"Standart vm {cloud_id} was created"
            " succesfully instead of the preemptible vm"
        )
    }


def get_err_vm_404_mes() -> dict:
    return {
        'code': '404',
        'message': 'Cant create vm in cloud'
    }


def get_err_vm_exist_mes() -> dict:
    return {
        'code': '403',
        'message:': (
            "It is impossible to create a preemptible"
            " vm because one has already been created"
        )
    }


def get_err_vm_not_pr_mes() -> dict:
    return {
        'code': '403',
        'message:': (
            "It is impossible to create a vm because"
            " the created machine is non-preemptable"
        )
    }


def get_success_del_vm_mes(cloud_vm_id: str) -> dict:
    return {
        'code': '204',
        'message:': f"vm {cloud_vm_id} was deleted succesfully"
    }


def get_err_del_vm_mes(cloud_vm_id: str) -> dict:
    return {
        'code': '403',
        'message:': f"vm {cloud_vm_id} does not exist"
    }


def get_err_del_cloud_vm_mes(cloud_vm_id: str) -> dict:
    return {
        'code': '403',
        'message:': f"cant delete vm {cloud_vm_id} in cloud"
    }


def get_err_del_cloud_port_mes(cloud_vm_id: str) -> dict:
    return {
        'code': '403',
        'message:': f"cant delete port on vm {cloud_vm_id} in cloud"
    }
