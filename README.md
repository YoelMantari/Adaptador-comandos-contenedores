# Adaptador--comandos-contenedores

### Estructura

```text
├── CHANGELOG.md
├── cli
│   └── container_exec.py
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
├── simple-app
│   └── Dockerfile
└── videos
    └── Sprint-1.mp4
```


## Sprint 2

### Paso 0
Instalar Kubernetes y Minikube

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

# Debe salir:
host: Running
kubelet: Running
apiserver: Running
```

Sino hay varias opciones:

Iniciar nuevamente Minikube:

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

### Paso 7

Ejecutar pruebas unitarias

```sh
pytest -v
```

## Sprint 1

### Estructura

```text
├── CHANGELOG.md
├── genera_changelog.py
├── README.md
└── simple-app
    └── Dockerfile
```


### Paso 0

Para definir la carpeta que usara Git para lanzar los hooks:

```sh
git config core.hooksPath .githooks
```

### Paso 1

Descagar la imagen de DockerHub

```sh
$ docker pull dirac22/simple-app:1.0.0
```

Ejecutar el contenedor:

```sh
$ docker run -it --name my-simple-app dirac22/simple-app:1.0.0
```

Estando ahora en "el terminal del contenedor"

Ejecutar ping (como ejemplo)
```sh
/# ping -c 4 google.com
```

### Paso 2
Ejecutar el script:
```sh
python3 cli/container_exec.py
```
Se mostrara un listado numerado de contenedores activos.
Por ejemplo (ps, ps aux, ping, ls, ... etc)