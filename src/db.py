import sqlite3
from datetime import datetime

import click # Biblioteca para criar comandos de linha de comandos
from flask import current_app, g # g armazena dados por requisição; current_app aponta para a app ativa


def get_db():
    if 'db' not in g: # Se ainda não houver uma conexão nesta requisição, cria uma
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # Usa o caminho definido na configuração
            detect_types=sqlite3.PARSE_DECLTYPES # Faz o SQLite reconhecer tipos de dados complexos
        )
        g.db.row_factory = sqlite3.Row # Permite aceder às colunas pelo nome (como um dicionário)

    return g.db # Retorna a conexão ativa


def close_db(e=None):
    db = g.pop('db', None) # Remove a conexão do objeto g

    if db is not None:
        db.close() # Se a conexão existia, fecha-a para libertar memória

def init_db():
    db = get_db() # Obtém a conexão com a base de dados

    # Abre o ficheiro SQL que contém as instruções de criação das tabelas
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) # Executa o script SQL para criar as tabelas


@click.command('init-db') # Define o nome do comando para o terminal
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas."""
    init_db() # Executa a criação das tabelas
    click.echo('Base de dados inicializada.') # Mensagem de sucesso no terminal


# Ensina o SQLite a converter datas (timestamp) de texto para objetos Python
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # Diz ao Flask para chamar close_db sempre que limpar o contexto da app (fim da requisição)
    app.teardown_appcontext(close_db)
    # Adiciona o comando 'flask init-db' à interface de linha de comandos da aplicação
    app.cli.add_command(init_db_command)