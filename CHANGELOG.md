# Sprint 1

## Dia 1


- **YoelMantari**: agregar plantilla para historias de usuario. Commit: `f658dc0`


## Dia 2
- **Dirac**: Agrega una simple app contenerizada. Commit: `16a0f80`
  

## Dia 3


- **Dirac**: Agrega post-commit y actualiza commit-msg. Commit: `34069b4`
- **Dirac**: Primera actualizacion Sprint 2. Commit: `55a6ef0`
- **Dirac**: Actualiza para inicio de Sprint 2. Commit: `154ee13`
  - Actualiza README para inicio de Sprint 2
  - Actualiza CHANGELOG para inicio de Sprint 2
  - Agrega script `genera_changelog.py` para automatizar actualizar el CHANGELOG

- **Dirac**: Agrega manifiesto deployment.yaml. Commit: `e38eddb`
  - Agrega manifiesto para despliegue enb Kubernetes
  - Se modifca el archivo Dockerfile para poder hacer el despliegue. 

- **Dirac**: Archivos iniciales para pruebas unitarias. Commit: `cdb4bbb`
  - Se agrego archivos `__init__.py` en carpeta `cli` y `tests`. Se agrego archivo ``requeriments.txt.` 

- **Dirac**: Agrega primer archivo de prueba. Commit: `a2b2cf6`
    - Ejecuta pruebas para metodos listar_contenedores y seleccionar_contenedor. 
    - Agrega manifiesto para despliegue enb Kubernetes.
    - Se modifca el archivo Dockerfile para poder hacer el despliegue. Commit: `e38eddb`

## Dia 4
- **YoelMantari**: listar pods de kubernetes desde la cli. Commit: `2fd72dd`
  - se añade la funcion listar_pods(), que imprime en forma enumerada los pods.

- **YoelMantari**: mejorar seleccion de contenedor por id o nombre. Commit: `c27325a`
  - se actualiza la funcion seleccionar_contenedor() para que se ingresar el id o nombre del contenedor en lugar de indice.

- **YoelMantari**: permitir seleccion de pod por numero desde la cli. Commit: `ab05660`
  - se añade la funcion seleccionar_pod() que solicita al usuario ingresar un numero que esta listado por indice. 

- **YoelMantari**: ejecutar comandos dentro de pods Kubernetes. Commit: `1c5ac21`
  - se implementa la funcion ejecutar_comando_k8s() que ejecuta un comando, detecta si es bash y permite interacion directa con pods desde la cli. 

- **YoelMantari**: adaptar main para soporte de docker y kubernetes. Commit: `583c94e`
  - se actualiza la el main para seleccionar tanto contenedores docker como en pods de kubernetes. 



- **Dirac**: Actualiza script para Sprint 2. Commit: `c98a4b5`
