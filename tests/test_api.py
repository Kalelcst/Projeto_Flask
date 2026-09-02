from models import db, Todo


def test_login_api_com_sucesso(client, create_user):
    create_user(email="apilogin@teste.com", password="senha123")

    response = client.post(
        "/api/login",
        json={"email": "apilogin@teste.com", "password": "senha123"},
    )

    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_api_credenciais_invalidas(client, create_user):
    create_user(email="apierro@teste.com", password="senha123")

    response = client.post(
        "/api/login",
        json={"email": "apierro@teste.com", "password": "senha_errada"},
    )

    assert response.status_code == 401


def test_login_api_sem_json(client):
    response = client.post("/api/login")

    assert response.status_code == 400


def test_acessar_perfil_sem_token(client):
    response = client.get("/api/profile")

    assert response.status_code == 401


def test_acessar_perfil_com_token_invalido(client):
    response = client.get(
        "/api/profile",
        headers={"Authorization": "Bearer token.invalido.aqui"},
    )

    assert response.status_code == 401


def test_acessar_perfil_com_token(client, api_token):
    response = client.get(
        "/api/profile",
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 200
    assert response.get_json()["email"] == "api@teste.com"


def test_criar_tarefa_sem_json(client, api_token):
    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 400


def test_criar_tarefa_com_sucesso(client, api_token):
    response = client.post(
        "/api/tasks",
        json={"content": "Tarefa via API"},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 201
    assert "task_id" in response.get_json()


def test_criar_tarefa_com_priority_invalida(client, api_token):
    response = client.post(
        "/api/tasks",
        json={"content": "Tarefa", "priority": "urgente"},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 400


def test_criar_tarefa_content_muito_longo(client, api_token):
    response = client.post(
        "/api/tasks",
        json={"content": "a" * 201},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 400


def test_listar_tarefas(client, api_token):
    client.post(
        "/api/tasks",
        json={"content": "Listar essa"},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 200
    tasks = response.get_json()
    assert any(t["content"] == "Listar essa" for t in tasks)


def test_atualizar_tarefa(client, api_token):
    create_response = client.post(
        "/api/tasks",
        json={"content": "Original"},
        headers={"Authorization": f"Bearer {api_token}"},
    )
    task_id = create_response.get_json()["task_id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"content": "Atualizada"},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 200


def test_deletar_tarefa(client, api_token):
    create_response = client.post(
        "/api/tasks",
        json={"content": "Para deletar"},
        headers={"Authorization": f"Bearer {api_token}"},
    )
    task_id = create_response.get_json()["task_id"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 200


def test_usuario_nao_acessa_tarefa_de_outro_via_api(client, app, create_user, api_token):
    outro_id = create_user(email="outroapi@teste.com", password="senha123")

    with app.app_context():
        tarefa = Todo(content="Privada via API", user_id=outro_id)
        db.session.add(tarefa)
        db.session.commit()
        task_id = tarefa.id

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"content": "hackeado"},
        headers={"Authorization": f"Bearer {api_token}"},
    )

    assert response.status_code == 404