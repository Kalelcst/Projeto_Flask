def test_registro_com_sucesso(client):
    response = client.post(
        "/register",
        data={"name": "Novo Usuário", "email": "novo@teste.com", "password": "senha123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Conta criada com sucesso".encode("utf-8") in response.data


def test_registro_com_email_duplicado(client, create_user):
    create_user(email="duplicado@teste.com")

    response = client.post(
        "/register",
        data={"name": "Outro", "email": "duplicado@teste.com", "password": "senha123"},
        follow_redirects=True,
    )

    assert "já está cadastrado".encode("utf-8") in response.data


def test_registro_com_senha_curta(client):
    response = client.post(
        "/register",
        data={"name": "Curto", "email": "curto@teste.com", "password": "123"},
        follow_redirects=True,
    )
    assert "pelo menos 6 caracteres".encode("utf-8") in response.data


def test_login_com_sucesso(client, create_user):
    create_user(email="login@teste.com", password="senha123")

    response = client.post(
        "/login",
        data={"email": "login@teste.com", "password": "senha123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Bem-vindo".encode("utf-8") in response.data


def test_login_com_senha_errada(client, create_user):
    create_user(email="errado@teste.com", password="senha123")

    response = client.post(
        "/login",
        data={"email": "errado@teste.com", "password": "senha_errada"},
        follow_redirects=True,
    )

    assert "inválidos".encode("utf-8") in response.data


def test_login_com_email_inexistente(client):
    response = client.post(
        "/login",
        data={"email": "naoexiste@teste.com", "password": "qualquer"},
        follow_redirects=True,
    )

    assert "inválidos".encode("utf-8") in response.data


def test_pagina_protegida_redireciona_sem_login(client):
    response = client.get("/", follow_redirects=True)

    assert "Faça login".encode("utf-8") in response.data


def test_logout(client, login_web):
    response = client.get("/logout", follow_redirects=True)

    assert "Logout realizado".encode("utf-8") in response.data