# Gerenciador de Tarefas
Projeto de gerenciamento de tarefas desenvolvido com Flask e SQLite.

## 📌 Funcionalidades

* Adicionar tarefas
* Atualizar tarefas
* Deletar tarefas
* Visualizar tarefas cadastradas
* Rota de verificação `/health`

---

## 🚀 Tecnologias utilizadas

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* HTML5
* CSS3
* Jinja2

---

## 📁 Estrutura do projeto

```bash
├── static/
│   └── css/
│       └── main.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── update.html
│
├── instance/
│   └── test.db
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Kalelcst/introducaoFlask.git
```

---

### 2. Entrar na pasta

```bash
cd introducaoFlask
```

---

### 3. Criar ambiente virtual

```bash
python -m venv env
```

---

### 4. Ativar ambiente virtual

Windows:

```bash
env\Scripts\activate
```

---

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 6. Executar aplicação

```bash
python app.py
```

---

## 🔍 Health Check

Rota utilizada para verificar se a aplicação está funcionando:

```bash
/health
```

Exemplo:

```json
{
  "status": "ok"
}
```