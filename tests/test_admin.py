def test_usuario_comum_nao_acessa_dashboard_admin(client, login_web):
    response = client.get("/admin/dashboard", follow_redirects=True)

    assert "Acesso restrito".encode("utf-8") in response.data


def test_admin_acessa_dashboard(client, login_admin_web):
    response = client.get("/admin/dashboard")

    assert response.status_code == 200


def test_admin_nao_pode_remover_proprio_admin(client, login_admin_web):
    response = client.post(
        f"/admin/user/toggle-admin/{login_admin_web}",
        follow_redirects=True,
    )

    assert "não pode alterar seu próprio nível".encode("utf-8") in response.data


def test_admin_nao_pode_excluir_propria_conta(client, login_admin_web):
    response = client.post(
        f"/admin/user/delete/{login_admin_web}",
        follow_redirects=True,
    )

    assert "não pode excluir sua própria conta".encode("utf-8") in response.data


def test_admin_promove_outro_usuario(client, login_admin_web, create_user):
    outro_id = create_user(email="outro@teste.com", password="senha123")

    response = client.post(
        f"/admin/user/toggle-admin/{outro_id}",
        follow_redirects=True,
    )

    assert "promovido para administrador".encode("utf-8") in response.data