def get_success_create_st_vm_mes(cloud_id: str) -> dict:
    """Get dict with success message if create standart vm

    :param cloud_id: vm id in cloud
    :type cloud_id: str
    :return: dict with success message
    :rtype: dict
    """
    return {
        'code': '201',
        'message:': f"Standart vm {cloud_id} was created succesfully"
    }


def get_success_create_pr_vm_mes(cloud_id: str) -> dict:
    """Get dict with success message if create preemptible vm

    :param cloud_id: vm id in cloud
    :type cloud_id: str
    :return: dict with success message
    :rtype: dict
    """
    return {
        'code': '201',
        'message:': (
            f"Preemptible vm {cloud_id}"
            " was created succesfully"
        )
    }


def get_success_create_st_vm_af_pr_mes(cloud_id: str) -> dict:
    """Get dict with success message if create
    standart vm after create preemptible vm

    :param cloud_id: vm id in cloud
    :type cloud_id: str
    :return: dict with success message
    :rtype: dict
    """
    return {
        'code': '201',
        'message:': (
            f"Standart vm {cloud_id} was created"
            " succesfully instead of the preemptible vm"
        )
    }


def get_err_vm_404_mes() -> dict:
    """Get dict with error message,
    when vm doesnt creates in cloud

    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '404',
        'message': 'Cant create vm in cloud'
    }


def get_err_vm_exist_mes() -> dict:
    """Get dict with error message,
    when vm has already been created

    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '403',
        'message:': (
            "It is impossible to create a preemptible"
            " vm because one has already been created"
        )
    }


def get_err_vm_not_pr_mes() -> dict:
    """Get dict with error message,
    when exist vm is non-preemptable

    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '403',
        'message:': (
            "It is impossible to create a vm because"
            " the created machine is non-preemptable"
        )
    }


def get_success_del_vm_mes(cloud_vm_id: str) -> dict:
    """Get dict with success message if vm was deleted

    :param cloud_vm_id: vm id in cloud
    :type cloud_vm_id: str
    :return: dict with success message
    :rtype: dict
    """
    return {
        'code': '204',
        'message:': f"vm {cloud_vm_id} was deleted succesfully"
    }


def get_err_del_vm_mes(cloud_vm_id: str) -> dict:
    """Get dict with error message,
    when cant deleted vm

    :param cloud_vm_id: vm id in cloud
    :type cloud_vm_id: str
    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '403',
        'message:': f"vm {cloud_vm_id} does not exist"
    }


def get_err_del_cloud_vm_mes(cloud_vm_id: str) -> dict:
    """Get dict with error message,
    when cant deleted vm in cloud

    :param cloud_vm_id: vm id in cloud
    :type cloud_vm_id: str
    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '403',
        'message:': f"cant delete vm {cloud_vm_id} in cloud"
    }


def get_err_del_cloud_port_mes(cloud_vm_id: str) -> dict:
    """Get dict with error message,
    when cant deleted port vm in cloud

    :param cloud_vm_id: vm id in cloud
    :type cloud_vm_id: str
    :return: dict with errors message
    :rtype: dict
    """
    return {
        'code': '403',
        'message:': f"cant delete port on vm {cloud_vm_id} in cloud"
    }
