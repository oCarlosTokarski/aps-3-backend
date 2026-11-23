# Aps 3 Back - End Unisenai

## Feito por:
Carlos Tokarski Borges Neto <br>
Dheyvid Bastos Pinto

## API de Eventos Acadêmicos

## API RESTful desenvolvida em Python utilizando FastAPI para gerenciamento de eventos acadêmicos, participantes e inscrições.

# 🛠️ Tecnologias

Python

FastAPI

Pydantic

SQLite

SQLAlchemy ORM

Uvicorn

# 📦 Instalação

Clone ou baixe o projeto e entre na pasta.

Instale as dependências:

pip install -r requirements.txt

# ▶️ Executando o projeto

Execute o seguinte comando:

uvicorn main:app --reload

# 📚 Swagger

A documentação da API é disponibilizada automaticamente pelo FastAPI.

Após iniciar o projeto, acesse:

http://127.0.0.1:8000/docs


No Swagger é possível visualizar e testar todas as rotas da API.

# 📌 Funcionalidades
## 📅 Eventos

Cadastrar evento

Listar eventos

Consultar evento

Atualizar evento

Excluir evento

# 👤 Participantes

Cadastrar participante

Listar participantes

Consultar participante

Atualizar participante

Excluir participante

# 📝 Inscrições

Inscrever participante em evento

Consultar participantes inscritos

Verificar disponibilidade de vagas

Impedir inscrições duplicadas

# ✅ Validações

A API possui validações para os dados enviados, como:

Campos obrigatórios

E-mail válido

Capacidade maior que zero

Data válida

Campos de texto não vazios (texto só com espaços também é recusado)

# ⚠️ Tratamento de erros

A API trata situações como:

Evento não encontrado

Participante não encontrado

Participante já inscrito

Evento sem vagas

Dados inválidos

# 📁 Estrutura do projeto

O projeto utiliza uma separação baseada em MVC:

controller — responsável pelas rotas da API

model — entidades do banco de dados e seus relacionamentos (SQLAlchemy)

schema — validação dos dados de entrada e saída (Pydantic)

service — responsável pelas regras de negócio e consultas ao banco

database.py — conexão com o SQLite, sessões e criação das tabelas

main.py — responsável pela inicialização da aplicação

```
projeto/
├── main.py
├── database.py
├── controller/   (evento, participante, inscricao, relatorio)
├── model/        (evento, participante, inscricao)
├── schema/       (evento, participante, inscricao, relatorio)
└── service/      (evento, participante, inscricao, relatorio)
```

# 💾 Armazenamento (Banco de dados)

Os dados são persistidos em um banco **SQLite** acessado com **SQLAlchemy ORM**.

O arquivo do banco é o `eventos.db`, criado automaticamente na raiz do projeto
na primeira execução (as tabelas também são criadas automaticamente em `main.py`).
Os dados continuam disponíveis após reiniciar a aplicação.
Para zerar os dados, basta apagar o arquivo `eventos.db`.

Tabelas:

- eventos (id, titulo, descricao, data, horario, local, capacidade, categoria)
- participantes (id, nome, email único, curso)
- inscricoes (id, evento_id, participante_id, data_inscricao) — com restrição
  de unicidade em (evento_id, participante_id)

Ao excluir um evento ou participante, as inscrições relacionadas também são
excluídas (cascade), evitando registros órfãos.
Não é permitido reduzir a capacidade de um evento abaixo do número de inscritos (409).

# 🛣️ Principais rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| POST/GET | /eventos | Cadastrar / listar eventos |
| GET/PUT/DELETE | /eventos/{id} | Consultar / atualizar / excluir evento |
| POST/GET | /participantes | Cadastrar / listar participantes |
| GET/PUT/DELETE | /participantes/{id} | Consultar / atualizar / excluir participante |
| POST | /eventos/{evento_id}/inscricoes/{participante_id} | Inscrever participante |
| GET | /eventos/{evento_id}/inscricoes | Listar inscritos do evento |
| GET | /relatorios/eventos/ocupacao | Relatório de ocupação |
| GET | /relatorios/eventos/categorias | Relatório por categoria |
| GET | /relatorios/participantes/cursos | Relatório por curso |

Códigos de erro principais: 404 (não encontrado), 409 (e-mail já cadastrado,
inscrição duplicada, evento sem vagas), 422 (dados inválidos).

# 📊 Relatórios

Todos são calculados dinamicamente com consultas SQLAlchemy (JOIN, GROUP BY, COUNT e SUM).

**Ocupação dos eventos** — `GET /relatorios/eventos/ocupacao`
Para cada evento: capacidade, total de inscritos, vagas disponíveis e percentual de ocupação (inclui eventos sem inscrições).

```json
[
  {
    "evento_id": 1,
    "titulo": "Workshop de Python",
    "capacidade": 40,
    "total_inscritos": 10,
    "vagas_disponiveis": 30,
    "percentual_ocupacao": 25.0
  }
]
```

**Eventos por categoria** — `GET /relatorios/eventos/categorias`
Por categoria: total de eventos, capacidade total e total de inscrições.

```json
[
  {
    "categoria": "Workshop",
    "total_eventos": 3,
    "capacidade_total": 120,
    "total_inscricoes": 95
  }
]
```

**Participação por curso** — `GET /relatorios/participantes/cursos`
Por curso: total de participantes cadastrados (sem repetir) e total de inscrições.

```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 80,
    "total_inscricoes": 150
  }
]
```

Se não houver registros, os relatórios retornam uma lista vazia (`[]`).

# 💡 Exemplos de utilização

Cadastrar participante (`POST /participantes`):

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "curso": "Engenharia de Software"
}
```

Cadastrar evento (`POST /eventos`):

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução à linguagem",
  "data": "2026-12-10",
  "horario": "19:00:00",
  "local": "Laboratório 3",
  "capacidade": 40,
  "categoria": "Workshop"
}
```

Inscrever (`POST /eventos/1/inscricoes/1`), resposta 201:

```json
{
  "id": 1,
  "evento_id": 1,
  "participante_id": 1,
  "data_inscricao": "2026-11-23"
}
```

Inscrição duplicada (409):

```json
{ "detail": "Participante já está inscrito neste evento." }
```

# 🧪 Como reproduzir os testes

1. Inicie a API com `uvicorn main:app --reload` e abra `http://127.0.0.1:8000/docs`.
2. Cadastre eventos e participantes e faça inscrições.
3. Teste os erros: inscrição duplicada, evento inexistente, evento sem vagas (use capacidade 1 e dois participantes) e e-mail repetido.
4. Consulte os 3 relatórios, depois altere ou exclua registros e consulte de novo para ver os valores mudarem.
5. Pare o servidor (Ctrl+C), inicie novamente e consulte `GET /eventos` para confirmar a persistência.
