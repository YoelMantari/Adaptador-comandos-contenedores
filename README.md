# Adaptador--comandos-contenedores

### Estructura

```text
├── CHANGELOG.md
├── cli
│   ├── container_exec.py
│   └── __init__.py
├── config.ini
├── deployment.yaml
├── genera_changelog.py
├── .githooks
│   ├── commit-msg
│   ├── post-commit
│   └── pre-commit
├── .github
│   └── ISSUE_TEMPLATE
│       └── historia-de-usuario.md
├── .gitignore
├── README.md
├── requirements.txt
├── simple-app
│   └── Dockerfile
├── tests
│   ├── __init__.py
│   └── test_container_exec.py
├── validaciones-dockerfile
└── videos
    ├── Sprint-1.mp4
    └── Sprint-2.mp4

```


### Paso 0

Para definir la carpeta que usara Git para lanzar los hooks:

```sh
$ git config core.hooksPath .githooks
```

Dar los permisos necesarios
```sh
$ chmod +x .githooks/commit-msg .githooks/post-commit .githooks/pre-commit
```

Instalar Docker, Kubernetes y Minikube

### Paso 1

Descargar la imagén de DockerHub. Nueva versión `1.1.0`

```sh
$ docker pull dirac22/simple-app:1.1.0
```

O construir la imagen:

```sh
docker build -t <user>/simple-app:1.1.0 ./simple-app
```

### Paso 2

Cargar la imagen en minikube

```sh
$ minikube image load dirac22/simple-app:1.1.0
```
    
Siempre asegurarse que Minikube este corriendo

```sh
$ minikube status

# Debe salir algo similar a:
host: Running
kubelet: Running
apiserver: Running
```

Puedes tambien iniciar nuevamente Minikube:

```sh
$ minikube start
```

O también inciar con una versión específica

```sh
$ minikube delete
$ minikube start --kubernetes-version=v1.33.1
```

Asegurate que Minikube este corriendo exitosamente.

### Paso 3

Crear namespace

```sh
$ kubectl create namespace desarrollo
```

Validar namespaces

```sh
$ kubectl get namespaces
```

Aplicar el manifiesto

```sh
$ kubectl apply -f deployment.yaml
```

### Paso 4

Verificar el Deployment
```sh
$ kubectl get deployments
```
    
Deberia salir el de simple-app-deployment

Verificar los pods

```sh
$ kubeclt get pods
# Debe salir el simple-app-deployment-<identificador>
```

### Paso 5

Probar un comando dentro del Pod

```sh
kubectl exec -it simple-app-deployment-<identificador> -- ping -c 4 google.com
```
### Paso 6
Ejecutar en un pode de kubernetes en modo k8s
```sh
python3 cli/container_exec.py --platform k8s
```
Ejecutar en un contenedor Docker en modo docker
```sh
python3 cli/container_exec.py --platform docker
```
Ejecutar en un pode de kubernetes en modo k8s y definiendo el namespace
```sh
python3 cli/container_exec.py --platform k8s --namespace desarrollo
```

### Paso 7

Ejecutar pruebas unitarias

```sh
pytest -v
```