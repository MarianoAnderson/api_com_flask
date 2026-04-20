from unittest.mock import patch
import pytest
from src.utils import potencia_quadrado, requires_role
from http import HTTPStatus

@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (0, 0), (-2, 4)])
def test_potencia_quadrada_sucesso(test_input, expected):
    assert potencia_quadrado(test_input) == expected

@pytest.mark.parametrize(
    "test_input,exc_class, msg", 
    [
        ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), 
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
    ],
)

def test_potencia_quadrada_falha(test_input,exc_class, msg):
    with pytest.raises(exc_class) as exc:
        potencia_quadrado(test_input)
    assert msg in str(exc.value)

def test_require_role_success(mocker):
    # Given 
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)    
    decoration_function = requires_role("admin")(lambda: "Success")

    # When
    result = decoration_function()

    # Then
    assert result == "Success"

def test_require_role_failure(mocker):  
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    decoration_function = requires_role("admin")(lambda: "Success")
    result = decoration_function()

    assert result == ({"message": "User dont have permission to perform this action"}, HTTPStatus.FORBIDDEN)
