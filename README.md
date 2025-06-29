# Adaptador--comandos-contenedores

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
python3 container_exec.py
```
Se mostrara un listado numerado de contenedores activos.
Por ejemplo (ps, ps aux, ping, ls, ... etc)