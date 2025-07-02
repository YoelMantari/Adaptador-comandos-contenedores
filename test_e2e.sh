#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

DOCKER_CONTAINER_NAME="e2e-test-container"
K8S_DEPLOYMENT_NAME="simple-app-deployment"
TEST_IMAGE_NAME="e2e-test-app:latest"

run_test() {
    echo -n "Test: $1... "
    output=$(eval "$2")
    
    if echo "$output" | grep -q "$3"; then
        echo -e "${GREEN}Paso prueba${NC}"
        return 0
    else
        echo -e "${RED}Fallo prueba${NC}"
        echo "Salida obtenida: "
        echo "$output"
        echo " "
        return 1
    fi
}

echo "Iniciando configuraciones iniciales"

echo "Limpiando recursos de pruebas anteriores..."
docker rm -f $DOCKER_CONTAINER_NAME 2>/dev/null
kubectl delete deployment $K8S_DEPLOYMENT_NAME 2>/dev/null

echo "Construyendo la imagen de prueba: $TEST_IMAGE_NAME"
docker build -t $TEST_IMAGE_NAME ./simple-app

echo "Desplegando contenedor Docker de prueba: $DOCKER_CONTAINER_NAME"
docker run -d --name $DOCKER_CONTAINER_NAME $TEST_IMAGE_NAME

echo "Cargando imagen a Minikube..."
minikube image load $TEST_IMAGE_NAME
echo "Desplegando en Kubernetes..."
kubectl apply -f deployment.yaml


echo "Configuraciones iniciales completada"
echo ""

echo "Iniciando Pruebas E2E"
failures=0

run_test "Alias 'ping_google' en Docker" \
         "echo -e '1\nping_google' | python3 cli/container_exec.py" \
         "bytes of data" \
         || failures=$((failures+1))

run_test "Alias 'list_root' en Kubernetes" \
         "echo -e '1\nlist_root' | python3 cli/container_exec.py -p k8s" \
         "etc" \
         || failures=$((failures+1))

run_test "Comando directo 'echo' en Docker" \
         "echo -e '1\necho HELLO DOCKER' | python3 cli/container_exec.py" \
         "HELLO DOCKER" \
         || failures=$((failures+1))
         
run_test "Comando directo 'echo' en Kubernetes" \
         "echo -e '1\necho HELLO K8S' | python3 cli/container_exec.py -p k8s" \
         "HELLO K8S" \
         || failures=$((failures+1))

echo ""


echo "Iniciando fase de teardown (Limpieza de contenedores y pods)"
echo "Limpiando recursos de prueba..."
docker rm -f $DOCKER_CONTAINER_NAME
kubectl delete deployment $K8S_DEPLOYMENT_NAME
echo "Limpieza Completa"
echo ""

if [ $failures -eq 0 ]; then
    echo -e "${GREEN}Todas las pruebas E2E pasaron exitosamente${NC}"
    exit 0
else
    echo -e "${RED}$failures prueba(s) E2E fallaron.${NC}"
    exit 1
fi