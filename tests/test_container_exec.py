import subprocess
from unittest.mock import Mock
import pytest
import sys
from cli.container_exec import (
    listar_contenedores,
    listar_pods,
    seleccionar_recurso,
    ejecutar_comando_docker,
    ejecutar_comando_k8s
)

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


def test_listar_pods_con_namespace(mocker):

    # Arrange
    texto_simulado = "NAME\npod-1\npod-2"
    mock_run = mocker.patch("cli.container_exec.subprocess.run")
    mock_run.return_value = Mock(stdout=texto_simulado)
    namespace_simulado = "desarrollo"

    # Act
    pods = listar_pods(namespace_simulado)

    # Assert
    comando_str = ["kubectl", "get", "pods", "-o", "custom-columns=NAME:.metadata.name", "-n", namespace_simulado]
    mock_run.assert_called_once_with(comando_str, stdout=subprocess.PIPE, text=True, check=True)
    assert pods == ["pod-1", "pod-2"]


@pytest.mark.parametrize(
        "tipo, entrada_usuario, id_esperado",
        [
            ("contenedor", "1", "id1"),
            ("pod", "2", "pod-2")
        ])
def test_seleccionar_recurso(mocker, tipo, entrada_usuario, id_esperado):
    # Arrange
    recursos_prueba = ["id1:img1", "pod-2"]
    mocker.patch("cli.container_exec.input", return_value=entrada_usuario)
    mocker.patch("cli.container_exec.print")

    # Act
    recurso = seleccionar_recurso(recursos_prueba, tipo)

    # Assert
    assert recurso == id_esperado

@pytest.mark.parametrize("comando", (["echo", "hola"], ["ping", "-c", "4", "google.com"]))
def test_ejecutar_comando_docker(mocker, comando):
    # Arrange
    mock_run = mocker.patch("cli.container_exec.subprocess.run")
    id_contenedor = "id_simulado"
    mock_print = mocker.patch("builtins.print")

    # Act
    ejecutar_comando_docker(id_contenedor, comando)
    comando_esperado = ["docker", "exec"] + [id_contenedor] + comando
    
    # Assert
    mock_run.assert_called_once_with(
        ["docker", "exec", id_contenedor] + comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert mock_print.call_count == 4
    

@pytest.mark.parametrize(
    "comando, namespace, espera_flags", 
    [
        (["echo", "hola"], "default", False),
        (["bash"], "desarrollo", True),
        (["sh", "-c", "ls"], None, True),
        (["ping", "google.com"], None, False)
    ]
)
def test_ejecutar_comando_k8s(mocker, comando, namespace, espera_flags):
    # Arrange
    mock_run = mocker.patch("cli.container_exec.subprocess.run")
    pod_name = "pod-simulado"
    
    # Act
    ejecutar_comando_k8s(pod_name, namespace, comando)
    
    # Assert - Construcción del comando esperado
    cmd_esperado = ["kubectl", "exec"]
    
    if namespace:
        cmd_esperado.extend(["-n", namespace])
    
    if espera_flags:
        cmd_esperado.extend(["-i", "-t"])
    
    cmd_esperado.extend([pod_name, "--"] + comando)
    
    # Verificación completa
    mock_run.assert_called_once_with(
        cmd_esperado,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr
    )