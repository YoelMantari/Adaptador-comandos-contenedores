import subprocess
import sys
import argparse
import configparser


def cargar_aliases(config_file="config.ini") -> dict:
    """
    Carga los alias desde un archivo de configuracion .ini.
    Devuelve un diccionario con los alias.
    """
    config = configparser.ConfigParser()
    if not config.read(config_file):
        return {}

    return dict(config.items('aliases'))


def listar_contenedores() -> list[str]:
    """
    Lista los contenedores docker en ejecucion usando docker ps
    retorna el id imagen por cada contenedor
    """
    comando = ["docker", "ps", "--format", "{{.ID}}: {{.Image}} - {{.Names}}"]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True)
    contenedores: list[str] = resultado.stdout.strip().split("\n")

    if not contenedores or contenedores == ['']:
        print("No hay contenedores en ejecucion.")
        sys.exit(0)
    return contenedores
    # print("\nContenedores activos:")
    # for i, cont in enumerate(contenedores):
    #     print(f"{i + 1}. {cont}")
    # return contenedores


def listar_pods(namespace: str | None) -> list[str]:
    """
    Lista pods en Kubernetes
    en ejecucion y los imprime
    """
    comando = ["kubectl", "get", "pods", "-o", "custom-columns=NAME:.metadata.name"]
    if namespace:
        comando.extend(["-n", namespace])
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True, check=True)
    pods = resultado.stdout.strip().splitlines()[1:]
    if not pods:
        print("No hay pods en el namespace actual.")
        sys.exit(0)
    # print("\nPods Kubernetes activos:")
    # for i, pod in enumerate(pods, 1):
    #     print(f"{i}. {pod}")
    return pods


def ejecutar_comando_docker(contenedor_id: str, comando: list[str]) -> None:
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
        print(f"'{entrada}' no es un numero valido, intentarlo de nuevo")


def ejecutar_comando_k8s(pod: str, namespace: str | None, comando: list[str]) -> None:
    """
    Ejecuta comando arbitrario dentro de un pod de Kubernetes.
    usando flags para interactuar en bash
    """
    cmd_base = ["kubectl", "exec"]
    if namespace:
        cmd_base.extend(["-n", namespace])
    flags = ["-i", "-t"] if comando and comando[0] in ("bash", "sh") else []
    cmd = cmd_base + flags + [pod, "--"] + comando
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


# --- Seleccionar recurso

def seleccionar_recurso(recursos: list[str], tipo_recurso: str) -> str:
    """
    Mostarmos una lista numerada de recursos (contenedores en docker o pods en kubernetes).
    Y devolvemos el nombre del recurso seleccionado por el usuario.
    """
    print(f"Recursos '{tipo_recurso}' disponibles:")
    for i, recurso in enumerate(recursos, 1):
        print(f"{i}. {recurso}")

    while True:
        try:
            indice = int(input(f"Selecciona un {tipo_recurso} por número: ")) - 1
            if 0 <= indice < len(recursos):
                if tipo_recurso == "contenedor":
                    print(f"salida: {recursos[indice].split(":")[0]}")
                    return recursos[indice].split(":")[0] # Para contenedores
                print(f"{recursos[indice]}")
                return recursos[indice] # Para pods
        except ValueError:
            print("Entrada inválida. Introduce un número")    

# ----------------------------------------------------------------------------------------

# --- Logica de manejo

def manejar_docker():
    """
    Para manejar ejecucion de comandos en Docker
    """
    recursos = listar_contenedores()
    if not recursos:
        return # Termina ejecución si no hay recursos
    recurso_id = seleccionar_recurso(recursos, "contenedor")
    comando_str = input(f"\nComando a ejecutar en el contenedor {recurso_id}: ").strip()
    if not comando_str:
        print("No se ingreso ningun comando")
        return
    ejecutar_comando_docker(recurso_id, comando_str.split())


def manejar_kubernetes(namespace: str | None):
    """
    Para manejar ejecucion de comandos en Kubernetes
    """
    recursos = listar_pods(namespace)
    if not recursos:
        return
    recurso = seleccionar_recurso(recursos, "pod")
    comando_str = input(f"\nComando a ejecutar en el pod {recurso}: ")
    if not comando_str:
        print("No se ingreso ningun comando")
        return
    ejecutar_comando_k8s(recurso, namespace, comando_str.split())

def main():
    """
    Funcion principal que parsea los argumentos y dirige el flujo del programa.
    """
    pars = argparse.ArgumentParser(
        description="Ejecuta comandos en Docker o Kubernetes"
    )
    pars.add_argument(
        "--platform", "-p",
        choices=["docker", "k8s"],
        default="docker",
        help="Plataforma: docker (por defecto) o k8s"
    )

    pars.add_argument(
        "--namespace", "-n",
        help="Especifica el namespace de Kubernetes a utilizar. (Solo para la plataforma k8s)"
    )

    args = pars.parse_args()

    if args.platform == "docker":
        # conts = listar_contenedores()
        # cid = seleccionar_contenedor(conts)
        # cmd = input("\nEscribe el comando a ejecutar dentro del contenedor: ").strip().split()
        # ejecutar_comando_docker(cid, cmd)
        manejar_docker()
    elif args.platform == "k8s":
        manejar_kubernetes(args.namespace)
    # else:
    #     pods = listar_pods(args.na)
    #     pod = seleccionar_pod(pods)
    #     cmd = input("\nEscribe el comando a ejecutar dentro del pod: ").strip().split()
    #     ejecutar_comando_k8s(pod, cmd)
    

if __name__ == "__main__":
    main()