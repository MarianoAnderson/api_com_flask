# API com Flask

## Descrição
Esta é uma API RESTful desenvolvida com Flask para gerenciamento de usuários, autenticação e roles (papéis). O projeto utiliza SQLAlchemy para ORM, Alembic para migrações de banco de dados, e JWT (JSON Web Tokens) para autenticação segura. Inclui testes unitários e de integração para garantir a qualidade do código.

## Status do Projeto
Projeto em desenvolvimento ativo e pode conter funcionalidades incompletas, bugs ou mudanças na estrutura.

## Tecnologias Utilizadas
- **Flask**: Framework web para Python
- **SQLAlchemy**: ORM para interação com banco de dados
- **Alembic**: Ferramenta para migrações de banco de dados
- **Flask-JWT-Extended**: Extensão para autenticação JWT
- **Pytest**: Framework para testes
- **Poetry**: Gerenciador de dependências e pacotes

## Pré-requisitos
- Python 3.11 ou superior
- Poetry instalado (para gerenciamento de dependências)

## Instalação
1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd api-com-flask
   ```

2. **Instale as dependências**:
   ```bash
   poetry install
   ```

3. **Ative o ambiente virtual**:
   ```bash
   poetry shell
   ```

4. **Configure o banco de dados**:
   - Execute as migrações para criar as tabelas:
     ```bash
     alembic upgrade head
     ```
   - Ou inicialize o banco de dados (se necessário):
     ```bash
     flask --app src.app init-db
     ```

## Configuração
- O banco de dados padrão é SQLite (`flaskbank.sqlite`) na pasta `instance/`.
- Para alterar configurações (como chave secreta ou URI do banco), edite o arquivo `src/config.py` ou passe variáveis de ambiente.
- Chave JWT: Configurada como "super-secret" por padrão (mude em produção).

## Execução
Para rodar a aplicação em modo de desenvolvimento:
```bash
flask --app src.app run --debug
```

Ou usando Poetry:
```bash
poetry run flask --app src.app run --debug
```

A API estará disponível em `http://127.0.0.1:5000`.

## Estrutura do Projeto
```
api-com-flask/
├── pyproject.toml          # Configuração do Poetry
├── README.md               # Este arquivo
├── instance/               # Dados da instância (banco de dados)
├── migrations/             # Migrações do Alembic
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── src/                    # Código fonte
│   ├── app.py              # Aplicação principal e modelos
│   ├── db.py               # Configuração do banco (não usado?)
│   ├── schema.sql          # Esquema SQL (não usado?)
│   ├── utils.py            # Utilitários (ex: decorador requires_role)
│   ├── controllers/        # Controladores da API
│   │   ├── auth.py         # Autenticação (login)
│   │   ├── user.py         # Gerenciamento de usuários
│   │   ├── role.py         # Gerenciamento de roles
│   │   └── post.py         # Posts (não implementado)
│   ├── models/             # Modelos adicionais (vazio)
│   └── views/              # Visualizações (vazio)
└── tests/                  # Testes
    ├── unit/               # Testes unitários
    └── integration/        # Testes de integração
```

## API Endpoints
A API possui os seguintes endpoints implementados:

### Autenticação
- `POST /auth/login`: Faz login e retorna um token JWT.
  - Corpo: `{"username": "string", "password": "string"}`
  - Resposta: `{"access_token": "jwt_token"}`

### Usuários
- `GET /users`: Lista todos os usuários (requer JWT e role 'admin').
  - Resposta: Lista de usuários com id, username e role.
- `POST /users`: Cria um novo usuário (requer JWT e role 'admin').
  - Corpo: `{"username": "string", "password": "string", "role_id": int}`
- `GET /users/<user_id>`: Obtém detalhes de um usuário específico.

### Roles
- `POST /roles`: Cria uma nova role.
  - Corpo: `{"name": "string"}`

**Nota**: Endpoints para posts ainda não estão implementados.

## Testes
Para executar todos os testes:
```bash
pytest
```

Para testes específicos:
- Unitários: `pytest tests/unit/`
- Integração: `pytest tests/integration/`

Os testes usam Pytest com mocks onde necessário.

## Desenvolvimento
- Para adicionar novos endpoints, crie controladores em `src/controllers/` e registre-os em `src/app.py`.
- Use Alembic para mudanças no banco: `alembic revision --autogenerate -m "mensagem"` seguido de `alembic upgrade head`.
- Adicione testes em `tests/unit/` ou `tests/integration/` conforme apropriado.

## Contribuição
Como o projeto está em desenvolvimento, contribuições são bem-vindas! Abra issues para discutir ideias ou bugs. Pull requests são aceitos após revisão.
