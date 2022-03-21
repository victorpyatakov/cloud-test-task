import pytest
from project.utils import create_vm, delete_vm
from app import db, VMInstanse


@pytest.fixture()
def clean_vm():
    instanse = db.session.query(VMInstanse).first()
    if instanse:
        delete_vm(instanse.cloud_id)


class TestVM:
    def test_create_standart(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=False)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Standart vm {instanse.cloud_id} was created succesfully"
            }
            assert instanse is not None
            assert instanse.name == "standart"
        assert result == expect

    def test_create_preemptible(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=True)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Preemptible vm {instanse.cloud_id} was created succesfully"
            }
            assert instanse is not None
            assert instanse.name == "preemptible"
        assert result == expect

    def test_create_st_after_pr(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_pr = create_vm(is_preemptible=True)
        if result_pr.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloudd"
            }
        else:
            instanse = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Preemptible vm {instanse.cloud_id} was created succesfully"
            }
            assert instanse is not None
            assert instanse.name == "preemptible"
        assert result_pr == expect

        result_st = create_vm(is_preemptible=False)
        if result_st.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': (
                    f"Standart vm {instanse.cloud_id} was created"
                    " succesfully instead of the preemptible vm"
                )
            }
            assert instanse is not None
            assert instanse.name == "standart"
        assert result_st == expect

    def test_create_st_after_st(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=False)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_1 = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Standart vm {instanse_1.cloud_id} was created succesfully"
            }
            assert instanse_1 is not None
            assert instanse_1.name == "standart"
        assert result == expect

        result_st = create_vm(is_preemptible=False)
        if result_st.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_2 = db.session.query(VMInstanse).first()
            expect = {
                'code': '403',
                'message:': (
                    "It is impossible to create a vm because"
                    " the created machine is non-preemptable"
                )
            }
            assert instanse_2 is not None
            assert instanse_2.name == "standart"
            assert instanse_1 == instanse_2
        assert result_st == expect

    def test_create_pr_after_st(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=False)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_1 = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Standart vm {instanse_1.cloud_id} was created succesfully"
            }
            assert instanse_1 is not None
            assert instanse_1.name == "standart"
        assert result == expect

        result_st = create_vm(is_preemptible=True)
        if result_st.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_2 = db.session.query(VMInstanse).first()
            expect = {
                'code': '403',
                'message:': (
                    "It is impossible to create a vm because"
                    " the created machine is non-preemptable"
                )
            }
            assert instanse_2 is not None
            assert instanse_2.name == "standart"
            assert instanse_1 == instanse_2
        assert result_st == expect

    def test_create_pr_after_pr(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=True)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_1 = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': (
                    f"Preemptible vm {instanse_1.cloud_id} was created succesfully"
                )
            }
            assert instanse_1 is not None
            assert instanse_1.name == "preemptible"
        assert result == expect

        result_st = create_vm(is_preemptible=True)
        if result_st.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse_2 = db.session.query(VMInstanse).first()
            expect = {
                'code': '403',
                'message:': (
                    "It is impossible to create a preemptible vm"
                    " because one has already been created"
                )
            }
            assert instanse_2 is not None
            assert instanse_2.name == "preemptible"
            assert instanse_1 == instanse_2
        assert result_st == expect

    def test_delete_vm(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=False)
        if result.get('code') == 404:
            expect = {
                'code': '404',
                'message:': "Cant create vm in cloud"
            }
        else:
            instanse = db.session.query(VMInstanse).first()
            expect = {
                'code': '201',
                'message:': f"Standart vm {instanse.cloud_id} was created succesfully"
            }
            assert instanse is not None
            assert instanse.name == "standart"
        assert result == expect

        cloud_vm_id = instanse.cloud_id
        result_del = delete_vm(cloud_vm_id)
        expect = {
            'code': '204',
            'message:': f"vm {cloud_vm_id} was deleted succesfully"
        }
        assert result_del == expect
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
