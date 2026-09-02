from models import db, Todo


def test_criar_tarefa(client, login_web):
    response = client.post(
        "/",
        data={"content": "Estudar Flask", "priority": "alta"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Estudar Flask".encode("utf-8") in response.data


def test_criar_tarefa_vazia_nao_permite(client, login_web):
    response = client.post(
        "/",
        data={"content": "   ", "priority": "media"},
        follow_redirects=True,
    )

    assert "não pode ficar vazia".encode("utf-8") in response.data


def test_editar_tarefa(client, app, login_web):
    client.post("/", data={"content": "Tarefa original", "priority": "baixa"})

    with app.app_context():
        task = Todo.query.filter_by(content="Tarefa original").first()
        task_id = task.id

    response = client.post(
        f"/update/{task_id}",
        data={"content": "Tarefa editada", "priority": "alta"},
        follow_redirects=True,
    )

    assert "Tarefa atualizada com sucesso".encode("utf-8") in response.data


def test_mover_tarefa_no_kanban(client, app, login_web):
    client.post("/", data={"content": "Mover essa", "priority": "media"})

    with app.app_context():
        task = Todo.query.filter_by(content="Mover essa").first()
        task_id = task.id

    response = client.post(f"/move-task/{task_id}/doing", follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Todo, task_id)
        assert task.status == "doing"


def test_deletar_tarefa(client, app, login_web):
    client.post("/", data={"content": "Deletar essa", "priority": "media"})

    with app.app_context():
        task = Todo.query.filter_by(content="Deletar essa").first()
        task_id = task.id

    client.post(f"/delete/{task_id}", follow_redirects=True)

    with app.app_context():
        assert db.session.get(Todo, task_id) is None


def test_usuario_nao_acessa_tarefa_de_outro(client, app, create_user):
    dono_id = create_user(email="dono@teste.com", password="senha123")

    with app.app_context():
        tarefa = Todo(content="Tarefa privada", user_id=dono_id)
        db.session.add(tarefa)
        db.session.commit()
        task_id = tarefa.id

    create_user(email="intruso@teste.com", password="senha123")
    client.post("/login", data={"email": "intruso@teste.com", "password": "senha123"})

    response = client.get(f"/update/{task_id}")

    assert response.status_code == 404