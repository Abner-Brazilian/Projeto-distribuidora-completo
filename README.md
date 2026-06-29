# Locadora Ribeiro — API REST

API REST completa para gerenciamento de equipamentos, clientes e aluguéis de uma locadora. Construída com Flask, PostgreSQL e autenticação JWT.

---

## Tecnologias

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- PostgreSQL
- python-dotenv

---

## Estrutura do Projeto

```
locadora-ribeiro/
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── migrations/
└── routes/
    ├── __init__.py
    ├── equipamentos.py
    ├── clientes.py
    ├── alugueis.py
    └── usuario.py
```

---

## Como Rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu_usuario/locadora-ribeiro.git
cd locadora-ribeiro
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```
DATABASE_URL=postgresql://usuario:senha@localhost/distribuidora
SECRET_KEY=sua_chave_secreta
```

**5. Execute as migrações**
```bash
flask db upgrade
```

**6. Rode o servidor**
```bash
python app.py
```

---

## Autenticação

Todas as rotas são protegidas por JWT. Para acessá-las:

**1. Faça login para obter o token:**
```
POST /login
```
```json
{
    "nome_usuario": "test",
    "senha": "test"
}
```

**2. Envie o token no header de todas as requisições:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

---

## Rotas

### Autenticação

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/login` | Realiza login e retorna o token JWT |

### Equipamentos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/equipamentos` | Lista todos os equipamentos |
| GET | `/equipamentos/buscar?nome=` | Busca equipamento por nome |
| POST | `/equipamentos` | Adiciona novo equipamento |
| PATCH | `/equipamentos/<id>/status` | Atualiza estado de uso |
| PATCH | `/equipamentos/<id>/valor` | Atualiza valor da diária |
| PATCH | `/equipamentos/<id>/categoria` | Atualiza categoria |
| DELETE | `/equipamentos/<id>` | Remove equipamento |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/clientes` | Lista todos os clientes |
| GET | `/clientes/buscar/nome?nome=` | Busca cliente por nome |
| GET | `/clientes/<id>/historico` | Histórico de aluguéis do cliente |
| POST | `/clientes` | Cadastra novo cliente |
| PUT | `/clientes/<id>` | Edita informações do cliente |
| DELETE | `/clientes/<id>` | Remove cliente |

### Aluguéis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/alugueis` | Lista todos os aluguéis |
| GET | `/alugueis/ativo` | Lista aluguéis em andamento |
| POST | `/alugueis` | Registra novo aluguel com cálculo automático do valor |
| PATCH | `/alugueis/<id>` | Registra devolução do equipamento |

### Relatórios

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/alugueis/relatorio/equipamentos` | Equipamentos mais alugados |
| GET | `/alugueis/relatorio/receita?data_inicio=&data_fim=` | Receita por período |
| GET | `/alugueis/relatorio/clientes` | Clientes mais ativos |

---

## Modelos

### Equipamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome do equipamento |
| descricao | String | Descrição |
| categoria | String | Categoria |
| valor_diario | Float | Valor da diária |
| em_uso | Boolean | Se está alugado no momento |

### Cliente
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome completo |
| telefone | String | Telefone de contato |
| cpf | String | CPF (11 dígitos) |
| email | String | E-mail de contato |

### Aluguel
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| cliente_id | Integer | Referência ao cliente |
| equipamento_id | Integer | Referência ao equipamento |
| data_inicio | Date | Data de início |
| data_fim | Date | Data prevista de devolução |
| valor_total | Float | Valor calculado automaticamente |
| ativo | Boolean | Se o aluguel está em andamento |

---

## Regras de Negócio

- Equipamento em uso não pode ser alugado novamente
- Equipamento em uso não pode ser deletado
- Cliente com aluguel ativo não pode ser deletado
- CPF deve ter 11 dígitos e ser único no sistema
- Data de devolução deve ser posterior à data de início
- Valor total é calculado automaticamente: dias x valor diário
- Ao registrar devolução, o equipamento é marcado como disponível automaticamente