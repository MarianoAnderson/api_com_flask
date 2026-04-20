import os
from datetime import datetime
from flask import Flask, current_app # Classe principal do framework
from flask_sqlalchemy import SQLAlchemy # Extensão para integração com bancos de dados usando SQLAlchemy
import click # Biblioteca para criar comandos de linha de comandos
from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate # gerenciamento de migrações de DB
from flask_jwt_extended import JWTManager # Gerenciamento de autenticação


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user: Mapped[list["User"]] = relationship(back_populates='role') # Relacionamento com a tabela User

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
    
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped['Role'] = relationship(back_populates='user') # Relacionamento com a tabela Role

    # Modo de exibição do objeto User, útil para depuração e logs
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, role_id={self.role_id!r})"

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"

@click.command('init-db') # Define o nome do comando para o terminal
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Base de dados inicializada.') # Mensagem de sucesso no terminal

def create_app(test_config=None):
    # Cria a app e define que ficheiros de configuração podem estar fora do pacote
    app = Flask(__name__, instance_relative_config=True)    
    # Configurações padrão (Chave de segurança e nome do banco de dados)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY="super-secret",
    )

    if test_config is None:
        # Carrega configurações reais do ficheiro config.py, se ele existir
        # silent=True significa que, se o ficheiro não existir, o programa não dá erro.
        app.config.from_pyfile('config.py', silent=True) 
    else:
        # Carrega configurações de teste caso sejam passadas como argumento
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path) # Garante que a pasta de instância existe
    except OSError:
        pass

    # Adiciona o comando 'flask init-db' à interface de linha de comandos da aplicação
    app.cli.add_command(init_db_command)
    # Inicializa a extensão SQLAlchemy com a aplicação
    db.init_app(app)
    # Inicializa a extensão de migração com a aplicação e o banco de dados
    migrate.init_app(app, db) 
    # Inicializa a extensão de autenticação com a aplicação
    jwt.init_app(app) 

    from src.controllers import user, auth, role # Importa os módulos de rotas
    

    app.register_blueprint(user.app) # Registra as rotas de usuário na aplicação
    app.register_blueprint(auth.app) # Registra as rotas de autenticação na aplicação
    app.register_blueprint(role.app) # Registra as rotas de papel na aplicação

    return app # Devolve a aplicação configurada


# flask --app src.app run --debug
# Caso O ambiente virtual não esteja ativado, ative-o com o comando: poetry run flask --app src.app run --debug
# flask --app src.app init-db 