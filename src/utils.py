from functools import wraps # Importa o decorador wraps para preservar as informações da função original
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from src.app import User, db

def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Obtém a identidade do usuário a partir do token JWT
            user_id = int(get_jwt_identity()) 
            # Verifica se o usuário existe no banco de dados, caso não, retorna 404
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {"message": "User dont have permission to perform this action"}, HTTPStatus.FORBIDDEN

            return f(*args, **kwargs)

        return wrapper

    return decorator

def potencia_quadrado(x):
    return x ** 2



# O decorador require_role é uma função que recebe o nome de uma função (role_name) e retorna um decorador (decorator). O decorador, por sua vez, recebe uma função (f) e retorna uma nova função (wrapper) que envolve a função original. A função wrapper verifica se o usuário autenticado tem a função necessária para acessar a rota protegida. Se o usuário não tiver a função necessária, ela retorna um erro 403 Forbidden. Caso contrário, ela chama a função original (f) e retorna seu resultado.