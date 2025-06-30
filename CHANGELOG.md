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

<<<<<<< Updated upstream
- **YoelMantari**: mejorar seleccion de contenedor por id o nombre. Commit: `c27325a`
  - se actualiza la funcion seleccionar_contenedor() para que se ingresar el id o nombre del contenedor en lugar de indice.

- **YoelMantari**: permitir seleccion de pod por numero desde la cli. Commit: `ab05660`
  - se añade la funcion seleccionar_pod() que solicita al usuario ingresar un numero que esta listado por indice. 

- **YoelMantari**: ejecutar comandos dentro de pods Kubernetes. Commit: `1c5ac21`
  - se implementa la funcion ejecutar_comando_k8s() que ejecuta un comando, detecta si es bash y permite interacion directa con pods desde la cli. 

- **YoelMantari**: adaptar main para soporte de docker y kubernetes. Commit: `583c94e`
  - se actualiza la el main para seleccionar tanto contenedores docker como en pods de kubernetes. 



## Dia 5

- **YoelMantari**: se agrega soporte para carga de alias desde config.ini. Commit: `518c082`
  - se implementa la funcion cargar_aliases() que permite leer alias definidos en un archivo ini. Commit: `feae786`

- **YoelMantari**: se agrega soporte para carga de alias desde config.ini. Commit: `02ca192`

- **YoelMantari**: permitir seleccion interactiva de pod por numero. Se agrega la funcion seleccionar_pod que solicita al usuario elegir un pod de una lista numerada. Commit: `f3d0fb9`

- **YoelMantari**: ejecutar comandos en docker con soporte para alias. Commit: `0adf775`

- **YoelMantari**: agregar soporte de alias en manejo de pods Kubernetes. Commit: `14f039d`

- **YoelMantari**: integrar soporte de alias en funcion principal. Se modifica main() para cargar alias desde config.ini y pasarlos a las funciones de ejecucion.. Commit: `641ea92`

- **YoelMantari**: agregar archivo confi.ini con alias de comandos. Commit: `511bb40`


- **Dirac**: Se agrega script para ejecutar prueba E2E. Commit: `d4b49da`
