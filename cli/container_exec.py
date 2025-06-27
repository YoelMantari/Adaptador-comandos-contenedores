import subprocess
import sys


def listar_contenedores() -> list[str]:
    """
    Lista los contenedores docker en ejecucion usando docker ps
    retorna el id imagen por cada contenedor
    """
    resultado = subprocess.run(
        ["docker", "ps", "--format", "{{.ID}}: {{.Image}} - {{.Names}}"],
        stdout=subprocess.PIPE,
        text=True
    )

    contenedores: list[str] = resultado.stdout.strip().split("\n")

    if not contenedores or contenedores == ['']:
        print("No hay contenedores en ejecucion.")
        sys.exit(0)

    print("\nContenedores activos:")
    for i, cont in enumerate(contenedores):
        print(f"{i + 1}. {cont}")
    return contenedores


def seleccionar_contenedor(contenedores: list[str]) -> str:
    """
    Permite al usuario selecciona un contenedor por indice,
    se lista los contenedores disponibles
    retorna el id del contenedor seleccionado
    """
    try:
        indice = int(input("\nSelecciona un contenedor (numero): ")) - 1
    except ValueError:
        print("Entrada invalida, debe ser un numero entero")
        sys.exit(1)

    if 0 <= indice < len(contenedores):
        return contenedores[indice].split(":")[0]
    else:
        print("Índice inválido.")
        sys.exit(1)