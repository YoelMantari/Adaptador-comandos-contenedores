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

