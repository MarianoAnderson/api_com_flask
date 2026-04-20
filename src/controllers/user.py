from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import User, db
from src.utils import requires_role
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id'],
    )
    db.session.add(user)
    db.session.commit()
    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id, 
            "username": user.username,
            "role":{
                "id": user.role.id,
                "name": user.role.name,
            }
            
        } 
        for user in users
    ]

@app.route('/', methods=['GET', 'POST'])
@jwt_required() # Protege a rota, exigindo um token de acesso válido para acessar
@requires_role('admin') # Verifica se o usuário tem a função de admin, caso contrário, retorna 403
def list_or_create_user():
    if request.method == 'POST':
        _create_user()
        return {"message": "User created successfully"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}

@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id) 
    return {"id": user.id, "username": user.username}

@app.route('/<int:user_id>', methods=['PATCH']) # Patch: atualização parcial de um recurso
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    
    # Obtém os dados JSON enviados na requisição (os campos a serem atualizados)
    data = request.json

    # Usa o inspect do SQLAlchemy para obter todas as atributos do User
    mapper = inspect(User)
    
    # Itera sobre cada atributo (coluna) do modelo User
    for column in mapper.attrs:
        # Verifica se a chave da coluna está presente nos dados enviados
        if column.key in data:
            # Atualiza o atributo do usuário com o novo valor
            setattr(user, column.key, data[column.key])
    
    # Salva as alterações no banco de dados
    db.session.commit()

    return {"id": user.id, "username": user.username}

@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}


# get_or_404: busca um recurso pelo ID e retorna 404 se não encontrado