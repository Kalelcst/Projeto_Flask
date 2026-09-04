# 📋 Gerenciador de Tarefas — Flask

[![Deploy](https://img.shields.io/badge/deploy-online-brightgreen)](https://projeto-flask-sy86.onrender.com)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1-black)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/tests-42%20passing-success)](#-testes-automatizados)
[![Coverage](https://img.shields.io/badge/coverage-87%25-yellowgreen)](#-testes-automatizados)

Aplicação web de gerenciamento de tarefas com quadro **Kanban**, autenticação de usuários, painel administrativo e API REST autenticada via JWT. Desenvolvida com Flask seguindo boas práticas de arquitetura: Application Factory, Blueprints e camada de Services.

**🔗 Acesse a aplicação ao vivo: [projeto-flask-sy86.onrender.com](https://projeto-flask-sy86.onrender.com)**

> ⚠️ A aplicação está hospedada no plano gratuito do [Render](https://render.com). Se ficar sem acesso por um tempo, o serviço "hiberna" — o primeiro carregamento após um período de inatividade pode levar de 30 a 50 segundos.

---

## 📌 Funcionalidades

**Usuário**
* Cadastro e login (sessão via cookie)
* Kanban de tarefas com 3 colunas (A Fazer / Fazendo / Concluído)
* Criar, editar, mover e excluir tarefas
* Definir prioridade da tarefa (baixa / média / alta)
* Busca de tarefas por texto
* Edição e exclusão do próprio perfil

**Administração**
* Dashboard com estatísticas (total de usuários, tarefas por status, admins)
* Gerenciamento de usuários (promover/remover admin, excluir conta)
* Acesso restrito por autorização em nível de rota

**API REST**
* Autenticação via JWT (token com expiração de 1 hora)
* CRUD completo de tarefas
* Validação de payload e tratamento de erros consistente

---

## 🚀 Tecnologias utilizadas

* **Python 3** / **Flask**
* **Flask-SQLAlchemy** — ORM
* **Flask-Migrate** (Alembic) — versionamento do banco de dados
* **Flask-WTF** — proteção CSRF
* **PyJWT** — autenticação da API
* **PostgreSQL** (produção) / **SQLite** (desenvolvimento)
* **Gunicorn** — servidor WSGI de produção
* **Pytest** — testes automatizados
* **HTML5, CSS3, Jinja2**
* **Render** — hospedagem (Web Service + PostgreSQL)

---

## 🏗️ Arquitetura

O projeto segue o padrão **Application Factory** com separação em camadas:

```
├── app.py                     # Application Factory
├── config.py                  # Configurações por ambiente (dev/prod/test)
├── models.py                  # Models SQLAlchemy (User, Todo)
├── auth.py                    # Autenticação JWT (decorator para API)
├── web_auth.py                # Autenticação de sessão (decorators para web)
├── api.py                     # Blueprint da API REST
├── make_admin.py              # Script CLI para promover um usuário a admin
│
├── routes/                    # Blueprints das rotas web
│   ├── auth_routes.py         # Login, cadastro, logout
│   ├── task_routes.py         # CRUD e Kanban de tarefas
│   ├── user_routes.py         # Perfil do usuário
│   └── admin_routes.py        # Painel administrativo
│
├── services/                  # Regras de negócio (camada de serviço)
│   ├── task_service.py
│   ├── user_service.py
│   └── admin_service.py
│
├── migrations/                # Versionamento do banco (Flask-Migrate)
│
├── tests/                     # Suíte de testes automatizados (Pytest)
│   ├── conftest.py            # Fixtures compartilhadas
│   ├── test_auth_web.py
│   ├── test_tasks_web.py
│   ├── test_user_web.py
│   ├── test_admin.py
│   └── test_api.py
│
├── templates/                 # Views Jinja2
├── static/css/                # Estilos
│
├── requirements.txt           # Dependências de produção
└── requirements-dev.txt       # Dependências de desenvolvimento (testes)
```

---

## ⚙️ Como executar o projeto localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Kalelcst/Projeto_Flask.git
cd Projeto_Flask
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv env
```

Windows:
```bash
env\Scripts\activate
```

Linux/Mac:
```bash
source env/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente (opcional em dev)

Em desenvolvimento, o app gera e persiste automaticamente uma `SECRET_KEY` local. Para produção, é **obrigatório** definir:

```bash
SECRET_KEY=uma-chave-secreta-forte
FLASK_ENV=production
DATABASE_URL=postgresql://usuario:senha@host:porta/banco   # opcional, usa SQLite se ausente
```

### 5. Criar o banco de dados

```bash
flask db upgrade
```

### 6. Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

### 7. (Opcional) Promover um usuário a administrador

```bash
python make_admin.py seuemail@exemplo.com
```

---

## ☁️ Deploy

A aplicação está hospedada no **Render**, com dois serviços:

* **Web Service** — executa `flask db upgrade && gunicorn app:app` a cada deploy, aplicando migrations pendentes automaticamente antes de subir o servidor
* **PostgreSQL** — banco gerenciado, conectado via variável de ambiente `DATABASE_URL`

O deploy é automático: qualquer `git push` na branch `main` dispara um novo build e deploy no Render.

---

## 🧪 Testes automatizados

O projeto conta com **42 testes automatizados** cobrindo autenticação, CRUD de tarefas, isolamento entre usuários, permissões administrativas e a API JWT — com aproximadamente **87% de cobertura de código**.

### Instalar dependências de teste

```bash
pip install -r requirements-dev.txt
```

### Rodar os testes

```bash
python -m pytest -v
```

### Rodar com relatório de cobertura

```bash
python -m pytest --cov=. --cov-report=term-missing
```

---

## 🔌 Documentação da API

Todas as rotas da API estão sob o prefixo `/api` e retornam JSON. As rotas protegidas exigem o header:

```
Authorization: Bearer <token>
```

### Autenticação

**`POST /api/login`**

Autentica um usuário e retorna um token JWT válido por 1 hora.

Request:
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

Response `200 OK`:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

Response `401 Unauthorized` — credenciais inválidas:
```json
{
  "message": "Credenciais inválidas"
}
```

---

### Perfil

**`GET /api/profile`** 🔒

Retorna os dados do usuário autenticado.

Response `200 OK`:
```json
{
  "id": 1,
  "name": "Usuário Exemplo",
  "email": "usuario@exemplo.com"
}
```

---

### Tarefas

**`GET /api/tasks`** 🔒

Lista todas as tarefas do usuário autenticado.

Response `200 OK`:
```json
[
  {
    "id": 1,
    "content": "Estudar Flask",
    "status": "todo",
    "priority": "alta"
  }
]
```

**`POST /api/tasks`** 🔒

Cria uma nova tarefa.

Request:
```json
{
  "content": "Nova tarefa",
  "priority": "media"
}
```
> `priority` é opcional (padrão: `"media"`). Valores aceitos: `baixa`, `media`, `alta`.

Response `201 Created`:
```json
{
  "message": "Tarefa criada com sucesso",
  "task_id": 5
}
```

Response `400 Bad Request` — validação:
```json
{
  "message": "Campo \"content\" não pode ficar vazio"
}
```

**`PUT /api/tasks/<id>`** 🔒

Atualiza uma tarefa existente (apenas o dono pode editar).

Request:
```json
{
  "content": "Tarefa atualizada",
  "priority": "alta"
}
```

Response `200 OK`:
```json
{
  "message": "Tarefa atualizada com sucesso"
}
```

Response `404 Not Found` — tarefa não existe ou não pertence ao usuário:
```json
{
  "message": "Tarefa não encontrada"
}
```

**`DELETE /api/tasks/<id>`** 🔒

Exclui uma tarefa (apenas o dono pode excluir).

Response `200 OK`:
```json
{
  "message": "Tarefa excluída com sucesso"
}
```

---

### Códigos de status utilizados

| Código | Significado |
|---|---|
| `200` | Sucesso |
| `201` | Recurso criado com sucesso |
| `400` | Erro de validação no payload enviado |
| `401` | Não autenticado / token inválido ou ausente |
| `404` | Recurso não encontrado (ou não pertence ao usuário) |
| `500` | Erro interno inesperado |

---

## 🔒 Segurança

* Senhas armazenadas com hash (Werkzeug `generate_password_hash`)
* Autenticação de sessão (web) e JWT com expiração (API)
* Proteção CSRF em todos os formulários
* Isolamento de dados entre usuários em nível de query
* Autorização por papel (usuário comum × administrador)
* `SECRET_KEY` nunca versionada no repositório
* Cookies de sessão com `HttpOnly` e `SameSite=Lax`; `Secure` habilitado automaticamente em produção
* Constraints de integridade no banco de dados (`status` e `priority` validados também no nível do banco)

---

## 🗄️ Banco de dados

O banco é gerenciado via **Flask-Migrate** (Alembic), com suporte nativo a **SQLite** (desenvolvimento) e **PostgreSQL** (produção), alternado automaticamente pela variável de ambiente `DATABASE_URL`.

Para gerar uma nova migration após alterar os models:

```bash
flask db migrate -m "descrição da alteração"
flask db upgrade
```

---

## 👤 Autor

Desenvolvido por [Kalel](https://github.com/Kalelcst)