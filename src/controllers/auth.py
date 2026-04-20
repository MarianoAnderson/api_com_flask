from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import inspect
from src.app import User, db
from http import HTTPStatus

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or user.password != password:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    # Cria um token de acesso JWT usando o ID do usuário como identidade
    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK



    # .scalar() é um método do SQLAlchemy que executa a consulta e retorna o primeiro resultado como um objeto Python. Se a consulta não encontrar nenhum resultado, ele retornará None.