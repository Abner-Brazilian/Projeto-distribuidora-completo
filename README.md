# Distribuidora de Equipamentos — API REST

API para gerenciamento de equipamentos, clientes e aluguéis de uma distribuidora.

---

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLite

---

## Estrutura do Projeto

```
distribuidora/
├── app.py
├── database.py
├── models.py
├── README.md
└── routes/
    ├── __init__.py
    ├── equipamentos.py
    ├── clientes.py
    └── alugueis.py
```

---

## Como Rodar

```bash
pip install flask flask-sqlalchemy
python app.py
```

---

## Rotas

### Equipamentos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/equipamentos` | Lista todos os equipamentos |
| GET | `/equipamentos/buscar?nome=` | Busca equipamento por nome ou categoria |
| POST | `/equipamentos` | Adiciona novo equipamento |
| PATCH | `/equipamentos/<id>/status` | Atualiza estado de uso |
| PATCH | `/equipamentos/<id>/valor` | Atualiza valor da diária |
| PATCH | `/equipamentos/<id>/categoria` | Atualiza categoria |
| DELETE | `/equipamentos/<id>` | Remove equipamento |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/clientes` | Lista todos os clientes |
| GET | `/clientes/buscar?nome=` | Busca cliente por nome |
| GET | `/clientes/<id>/historico` | Histórico de aluguéis do cliente |
| POST | `/clientes` | Cadastra novo cliente |
| PATCH | `/clientes/<id>` | Edita informações do cliente |
| DELETE | `/clientes/<id>` | Remove cliente |

### Aluguéis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/alugueis` | Lista todos os aluguéis |
| GET | `/alugueis/ativos` | Lista aluguéis em andamento |
| POST | `/alugueis` | Registra novo aluguel |
| PATCH | `/alugueis/<id>/devolver` | Marca equipamento como devolvido |

---

## Modelos

### Equipamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome do equipamento |
| descricao | String | Descrição do equipamento |
| categoria | String | Categoria do equipamento |
| valor_diario | Float | Valor da diária |
| em_uso | Boolean | Se está alugado no momento |

### Cliente
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome completo |
| telefone | String | Telefone de contato |
| cpf | String | CPF do cliente |
| email | String | E-mail de contato |

### Aluguel
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| cliente_id | Integer | Referência ao cliente |
| equipamento_id | Integer | Referência ao equipamento |
| data_inicio | Date | Data de início do aluguel |
| data_fim | Date | Data prevista de devolução |
| ativo | Boolean | Se o aluguel está em andamento |

---

## Roadmap

### Fase 1 — Robustez ⚙️
- [ ] Tratamento de erros — respostas adequadas para body incompleto ou dados inválidos
- [ ] Validação de CPF
- [ ] Validação de formato de telefone
- [ ] Verificação de conflito — impedir aluguel de equipamento já em uso

### Fase 2 — Novas Funcionalidades 🚀
- [ ] Cálculo automático do valor total (dias alugados x valor diário)
- [ ] Rota de devolução — marca aluguel como inativo e equipamento como disponível automaticamente
- [ ] Relatório de equipamentos mais alugados
- [ ] Relatório de receita por período
- [ ] Relatório de clientes mais ativos

### Fase 3 — Produção 🌐
- [ ] Migração para PostgreSQL
- [ ] Autenticação com JWT
- [ ] Variáveis de ambiente para senhas e configurações
- [ ] Deploy em servidor (Railway ou Render)