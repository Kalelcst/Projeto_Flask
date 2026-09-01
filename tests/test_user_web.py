from models import db, User


def test_ver_proprio_perfil(client, login_web):
    response = client.get("/users")

    assert response.status_code == 200


def test_editar_proprio_perfil_com_sucesso(client, login_web):
    response = client.post(
        f"/user/update/{login_web}",
        data={"name": "Nome Atualizado", "email": "novoemail@teste.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Perfil atualizado com sucesso".encode("utf-8") in response.data


def test_editar_perfil_sem_nome(client, login_web):
    response = client.post(
        f"/user/update/{login_web}",
        data={"name": "   ", "email": "email@teste.com"},
        follow_redirects=True,
    )

    assert "Nome é obrigatório".encode("utf-8") in response.data


def test_editar_perfil_sem_email(client, login_web):
    response = client.post(
        f"/user/update/{login_web}",
        data={"name": "Nome Válido", "email": "   "},
        follow_redirects=True,
    )

    assert "Email é obrigatório".encode("utf-8") in response.data


def test_editar_perfil_com_email_ja_cadastrado(client, app, login_web, create_user):
    create_user(email="jaexiste@teste.com", password="senha123")

    response = client.post(
        f"/user/update/{login_web}",
        data={"name": "Nome Válido", "email": "jaexiste@teste.com"},
        follow_redirects=True,
    )

    assert "já está cadastrado".encode("utf-8") in response.data


def test_usuario_nao_pode_editar_perfil_de_outro(client, app, login_web, create_user):
    outro_id = create_user(email="outro@teste.com", password="senha123")

    response = client.post(
        f"/user/update/{outro_id}",
        data={"name": "Hackeado", "email": "hackeado@teste.com"},
        follow_redirects=True,
    )

    assert "Acesso negado".encode("utf-8") in response.data

    with app.app_context():
        outro = db.session.get(User, outro_id)
        assert outro.name != "Hackeado"


def test_deletar_propria_conta(client, app, login_web):
    response = client.post(
        f"/user/delete/{login_web}",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "excluída com sucesso".encode("utf-8") in response.data

    with app.app_context():
        assert db.session.get(User, login_web) is None


def test_usuario_nao_pode_deletar_conta_de_outro(client, app, login_web, create_user):
    outro_id = create_user(email="protegido@teste.com", password="senha123")

    response = client.post(
        f"/user/delete/{outro_id}",
        follow_redirects=True,
    )

    assert "Acesso negado".encode("utf-8") in response.data

    with app.app_context():
        assert db.session.get(User, outro_id) is not None


def test_pagina_perfil_exige_login(client):
    response = client.get("/users", follow_redirects=True)

    assert "Faça login".encode("utf-8") in response.data