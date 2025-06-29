import subprocess
from unittest.mock import Mock
import pytest
from cli.container_exec import listar_contenedores, seleccionar_contenedor

def test_listar_contenedores_existentes(mocker):

    # Arrange
    texto_simulado = "id1: imagen1 - nombre1\nid2: imagen2 - nombre2"
    resultado_mock = Mock()
    resultado_mock.stdout = texto_simulado
    mock_run = mocker.patch("cli.container_exec.subprocess.run", return_value=resultado_mock)
    mock_print = mocker.patch("builtins.print")

    # Act
    contenedores = listar_contenedores()

    # Assert
    assert contenedores == ["id1: imagen1 - nombre1", "id2: imagen2 - nombre2"]

    mock_run.assert_called_once_with(
        ["docker", "ps", "--format", "{{.ID}}: {{.Image}} - {{.Names}}"],
        stdout=subprocess.PIPE,
        text=True
    )

    assert mock_print.call_count > 0


def test_listar_contenedores_no_hay(mocker):

    # Arrange
    resultado_mock = Mock()
    resultado_mock.stdout = ""
    mocker.patch("cli.container_exec.subprocess.run", return_value=resultado_mock)
    mocker.patch("builtins.print")

    # Act
    with pytest.raises(SystemExit) as e:
        listar_contenedores()

    assert e.type == SystemExit
    assert e.value.code == 0


CONTENEDORES=["id1: img1", "id2: img2"]

@pytest.mark.parametrize(
    "entrada, id_esperado, falla",
    [
        ("1", "id1", False), # Entrada valida
        ("2", "id2", False), # Entrada valida
        ("3", "id3", True), # Entrada invalida: solo hay dos contenedores
        ("abc", True, True), # Entrada invalida: Valores en parametro 1 y 2 no validos
        ("0", 4, True)  # Entrada invalida: Valores en parametro 1 y 2 no validos
    ]
)
def test_seleccionar_contenedor(mocker, entrada, id_esperado, falla):
    # Arrange
    mocker.patch("builtins.input", return_value=entrada)
    mocker.patch("builtins.print")

    # Act and Arrange
    if falla:
        with pytest.raises(SystemExit) as e:
            seleccionar_contenedor(CONTENEDORES)
    else:
        contenedor_id = seleccionar_contenedor(CONTENEDORES)
        assert contenedor_id == id_esperado