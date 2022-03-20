import pytest
from project.utils import get_cloud_vm, create_vm, delete_vm
from app import db, VMInstanse

@pytest.fixture()
def clean_vm():
    instanse = db.session.query(VMInstanse).first()
    if instanse:
        delete_vm(instanse.cloud_id)

class TestVM():
    
    def test_create_standart(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=False)
        assert result == "cоздана стадарт вм"
        instanse = db.session.query(VMInstanse).first()
        assert not instanse is None
        assert instanse.name == "standart"

    def test_create_preemptible(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result = create_vm(is_preemptible=True)
        assert result == "cоздана вытесняемая вм"
        instanse = db.session.query(VMInstanse).first()
        assert not instanse is None
        assert instanse.name == "preemptible"

    def test_create_st_after_pr(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_pr = create_vm(is_preemptible=True)
        assert result_pr == "cоздана вытесняемая вм"
        instanse = db.session.query(VMInstanse).first()
        assert not instanse is None
        assert instanse.name == "preemptible"

        result_st = create_vm(is_preemptible=False)
        assert result_st == "cоздана стадарт вм вместо вытесняемой"
        instanse = db.session.query(VMInstanse).first()
        assert not instanse is None
        assert instanse.name == "standart"



    def test_create_st_after_st(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_st = create_vm(is_preemptible=False)
        assert result_st == "cоздана стадарт вм"
        instanse_1 = db.session.query(VMInstanse).first()
        assert not instanse_1 is None
        assert instanse_1.name == "standart"

        result_st = create_vm(is_preemptible=False)
        assert result_st == "нельзя создать вм так как созданая машина является не вытесянемой"
        instanse_2 = db.session.query(VMInstanse).first()
        assert not instanse_2 is None
        assert instanse_2.name == "standart"
        assert instanse_1 == instanse_2

    def test_create_pr_after_st(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_st = create_vm(is_preemptible=False)
        assert result_st == "cоздана стадарт вм"
        instanse_1 = db.session.query(VMInstanse).first()
        assert not instanse_1 is None
        assert instanse_1.name == "standart"

        result_st = create_vm(is_preemptible=True)
        assert result_st == "нельзя создать вм так как созданая машина является не вытесянемой"
        instanse_2 = db.session.query(VMInstanse).first()
        assert not instanse_2 is None
        assert instanse_2.name == "standart"
        assert instanse_1 == instanse_2

    def test_create_pr_after_pr(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_pr = create_vm(is_preemptible=True)
        assert result_pr == "cоздана вытесняемая вм"
        instanse_1 = db.session.query(VMInstanse).first()
        assert not instanse_1 is None
        assert instanse_1.name == "preemptible"

        result_pr= create_vm(is_preemptible=True)
        assert result_pr == "нельзя создать вытесняемую вм так как уже создана такая"
        instanse_2 = db.session.query(VMInstanse).first()
        assert not instanse_2 is None
        assert instanse_2.name == "preemptible"
        assert instanse_1 == instanse_2

    def test_delete_vm(self, clean_vm):
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None
        result_st = create_vm(is_preemptible=False)
        assert result_st == "cоздана стадарт вм"
        instanse = db.session.query(VMInstanse).first()
        assert not instanse is None
        assert instanse.name == "standart"
        cloud_vm_id = instanse.cloud_id
        result_del = delete_vm(cloud_vm_id)
        assert result_del == f'vm {cloud_vm_id} was deleted succesfully'
        instanse = db.session.query(VMInstanse).first()
        assert instanse is None



