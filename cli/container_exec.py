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


def listar_pods() -> list[str]:
    """
    Lista pods en Kubernetes
    """
    resultado = subprocess.run(
        ["kubectl", "get", "pods", "-o", "custom-columns=NAME:.metadata.name"],
        stdout=subprocess.PIPE, text=True, check=True
    )
    pods = resultado.stdout.strip().splitlines()[1:]  
    if not pods:
        print("No hay pods en el namespace actual.")
        sys.exit(0)
    print("\nPods Kubernetes activos:")
    for i, pod in enumerate(pods, 1):
        print(f"{i}. {pod}")
    return pods


def seleccionar_contenedor(contenedores: list[str]) -> str:
    """
    Solicita al usuario que ingrese un ID o nombre 
    valido hasta que lo haga correctamente.
    Devuelve el ID del contenedor correspondiente.
    """
    while True:
        entrada = input("\nSelecciona un contenedor (ID o nombre): ").strip()
        for cont in contenedores:
            try:
                cid, resto = cont.split(":", 1)
                nombre = resto.split(" - ")[1].strip()
                if entrada == cid or entrada == nombre:
                    return cid
            except (IndexError, ValueError):
                continue  # ignorar formatos inesperados
        print(f"'{entrada}' no coincide con ningun ID o nombre listado, intentarlo de nuevo")


def ejecutar_comando(contenedor_id: str, comando: list[str]) -> None:
    """
    Ejecuta comando arbitrario dentro del contenedor docker.
    Se toma el id o nombre del contenedor del docker, y el comando
    a ejecutar.
    """
    resultado = subprocess.run(
        ["docker", "exec", contenedor_id] + comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("\nSalida estandar:")
    print(resultado.stdout)
    print("Errores:")
    print(resultado.stderr)


def seleccionar_pod(pods: list[str]) -> str:
    """
    Solicita al usuario que seleccione un pod por número.
    Devuelve el nombre del pod.
    """
    while True:
        entrada = input("\nSelecciona un pod (numero): ").strip()
        if entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(pods):
                return pods[idx]
        print(f"'{entrada}' no es un número valido. Intenta nuevamente.")


def main():
    contenedores = listar_contenedores()
    contenedor_id = seleccionar_contenedor(contenedores)
    comando = input("\nEscribe el comando a ejecutar dentro del contenedor: ").strip().split()
    ejecutar_comando(contenedor_id, comando)


if __name__ == "__main__":
    main()