# Adaptador--comandos-contenedores

**Video para la PC5:**

https://youtu.be/OaViE2hYSiU

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

---

### Autenticación de usuarios en contenedores

Construir la imagen

```sh
docker build -t dirac/simple-app:1.6.0 ./simple-app
```

Correr un contenedor a partir de la imagen:

```sh
docker run -d --name contenedor-usuario dirac22/simple-app:latest
```

Para ejecutar comandos dentro del contenedor y ver el usuario:

```sh
docker exec -it contenedor-usuario sh
```

Dentro podemos escribir

```sh
whoami
```

Y nos saldrá el usuario `dirac`. Si por ejemplo queremos crear un archivo en una carpeta restringida como `/etc`

```sh
touch etc/test.txt
```

Saldrá permiso denegado.


### **TLS** y conexiones seguras

Crear el directorio de trabajo

```sh
$ mkdir -p ~/docker-tls
$ ~/docker-tls
```

#### Crear la CA 
Creamos la Autoridad certificadora, aquí vamos a generar una clave privada RSA de 4096 bits cifrada mediante AES-256 longitud de 256
  

```sh
$ openssl genrsa -aes256 -out ca-key.pem 4096
```

Crear certificado publico para la CA
Creamos un certificado auto firmado valido para un año. Este certificado será usado para firmar certificados del servidor y del cliente.

```sh
$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
```

#### Generar certificado para el servidor

```sh
$ openssl genrsa -out server-key.pem 4096
```
  

Crear CSR `hostname=127.0.0.1`
Creamos una CSR (Solicitud de firma de Certificado) he indico la IP de mi máquina virtual Ubuntu. Esta IP es la que será accedida por mi maquina host que hará de cliente remoto.

```sh
$ openssl req -subj "/CN=192.168.81.9" -sha256 -new -key server-key.pem -out server.csr
```

Especificar extensiones
Aquí especificamos para qué IP es válido el certificado. Y declaramos que el certificado será usado por el servidor.

```sh
$ echo subjectAltName = IP:192.168.81.9 > extfile.cnf
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```

  
Firmar el certificado
Aquí se firma la solicitud `server.csr` usando la CA para emitir el certificado final del servidor.
  
```sh

$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out server-cert.pem -extfile extfile.cnf
```
  
#### Generar el certificado para el cliente

  
Algo similar para el certificado para el cliente. En nuestro caso será mi maquina host Windows.

- Genero una clave privada de 4096 bit para el cliente usando RSA
- Creamos una CSR para el cliente
- Indicamos que este certificado se usará para la autenticación del cliente.

```sh
$ openssl genrsa -out key.pem 4096
$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf

```

  Se firma la CSR del cliente

```sh
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out cert.pem -extfile extfile-client.cnf
```

#### Proteger los archivos

- Solo lectura para el propietario
- Solo lectura para todos

```sh
$ chmod 0400 ca-key.pem key.pem server-key.pem
$ chmod 0444 ca.pem server-cert.pem cert.pem
```

  
#### Iniciar Docker con TLS

Detenemos el servicio docker

```sh
sudo systemctl stop docker
```

  Iniciamos el daemon Docker de forma manual:

```sh
sudo dockerd \
--tlsverify \
--tlscacert=ca.pem \
--tlscert=server-cert.pem \
--tlskey=server-key.pem \
-H=0.0.0.0:2376
```

#### En la maquina cliente remota
  

```sh
$ docker --tlsverify \
--tlscacert=ca.pem \
--tlscert=cert.pem \
--tlskey=key.pem \
-H=tcp://192.168.81.9:2376 version
```

  

```sh
$ export DOCKER_HOST=tcp://192.168.81.9:2376
$ export DOCKER_TLS_VERIFY=1 

# En mi Windows:
$ export DOCKER_CERT_PATH="C:\Users\mitch\Documents\docker-tls"
```

#### Prueba en maquina cliente Windows

```sh
$ docker ps
$ docker ps -a
```

### **TLS** y conexiones seguras

Crear el directorio de trabajo

```sh
$ mkdir -p ~/docker-tls
$ ~/docker-tls
```

#### Crear la CA 
Creamos la Autoridad certificadora, aquí vamos a generar una clave privada RSA de 4096 bits cifrada mediante AES-256 longitud de 256
  

```sh
$ openssl genrsa -aes256 -out ca-key.pem 4096
```

Crear certificado publico para la CA
Creamos un certificado auto firmado valido para un año. Este certificado será usado para firmar certificados del servidor y del cliente.

```sh
$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
```

#### Generar certificado para el servidor

```sh
$ openssl genrsa -out server-key.pem 4096
```
  

Crear CSR `hostname=127.0.0.1`
Creamos una CSR (Solicitud de firma de Certificado) he indico la IP de mi máquina virtual Ubuntu. Esta IP es la que será accedida por mi maquina host que hará de cliente remoto.

```sh
$ openssl req -subj "/CN=192.168.81.9" -sha256 -new -key server-key.pem -out server.csr
```

Especificar extensiones
Aquí especificamos para qué IP es válido el certificado. Y declaramos que el certificado será usado por el servidor.

```sh
$ echo subjectAltName = IP:192.168.81.9 > extfile.cnf
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```

  
Firmar el certificado
Aquí se firma la solicitud `server.csr` usando la CA para emitir el certificado final del servidor.
  
```sh

$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out server-cert.pem -extfile extfile.cnf
```
  
#### Generar el certificado para el cliente

  
Algo similar para el certificado para el cliente. En nuestro caso será mi maquina host Windows.

- Genero una clave privada de 4096 bit para el cliente usando RSA
- Creamos una CSR para el cliente
- Indicamos que este certificado se usará para la autenticación del cliente.

```sh
$ openssl genrsa -out key.pem 4096
$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf

```

  Se firma la CSR del cliente

```sh
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out cert.pem -extfile extfile-client.cnf
```

#### Proteger los archivos

- Solo lectura para el propietario
- Solo lectura para todos

```sh
$ chmod 0400 ca-key.pem key.pem server-key.pem
$ chmod 0444 ca.pem server-cert.pem cert.pem
```

  
#### Iniciar Docker con TLS

Detenemos el servicio docker

```sh
sudo systemctl stop docker
```

  Iniciamos el daemon Docker de forma manual:

```sh
sudo dockerd \
--tlsverify \
--tlscacert=ca.pem \
--tlscert=server-cert.pem \
--tlskey=server-key.pem \
-H=0.0.0.0:2376
```

#### En la maquina cliente remota
  

```sh
$ docker --tlsverify \
--tlscacert=ca.pem \
--tlscert=cert.pem \
--tlskey=key.pem \
-H=tcp://192.168.81.9:2376 version
```

  

```sh
$ export DOCKER_HOST=tcp://192.168.81.9:2376
$ export DOCKER_TLS_VERIFY=1 

# En mi Windows:
$ export DOCKER_CERT_PATH="C:\Users\mitch\Documents\docker-tls"
```

#### Prueba en maquina cliente Windows

```sh
$ docker ps
$ docker ps -a
```

### **TLS** y conexiones seguras

Crear el directorio de trabajo

```sh
$ mkdir -p ~/docker-tls
$ ~/docker-tls
```

#### Crear la CA 
Creamos la Autoridad certificadora, aquí vamos a generar una clave privada RSA de 4096 bits cifrada mediante AES-256 longitud de 256

```sh
$ openssl genrsa -aes256 -out ca-key.pem 4096
```

Creamos un certificado auto firmado valido para un año. Este certificado será usado para firmar certificados del servidor y del cliente.

```sh
$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
```

#### Generar certificado para el servidor

```sh
$ openssl genrsa -out server-key.pem 4096
```
  
Creamos una CSR (Solicitud de firma de Certificado) he indico la IP de mi máquina virtual Ubuntu. Esta IP es la que será accedida por mi maquina host que hará de cliente remoto.

```sh
$ openssl req -subj "/CN=192.168.81.9" -sha256 -new -key server-key.pem -out server.csr
```

Aquí especificamos para qué IP es válido el certificado. Y declaramos que el certificado será usado por el servidor.

```sh
$ echo subjectAltName = IP:192.168.81.9 > extfile.cnf
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```


Aquí se firma la solicitud `server.csr` usando la CA para emitir el certificado final del servidor.
  
```sh

$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out server-cert.pem -extfile extfile.cnf
```
  
#### Generar el certificado para el cliente

  
Algo similar para el certificado para el cliente. En nuestro caso será mi maquina host Windows.

- Genero una clave privada de 4096 bit para el cliente usando RSA
- Creamos una CSR para el cliente
- Indicamos que este certificado se usará para la autenticación del cliente.

```sh
$ openssl genrsa -out key.pem 4096
$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf
```

Se firma la CSR del cliente

```sh
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
-CAcreateserial -out cert.pem -extfile extfile-client.cnf
```

#### Proteger los archivos

- Solo lectura para el propietario
- Solo lectura para todos

```sh
$ chmod 0400 ca-key.pem key.pem server-key.pem
$ chmod 0444 ca.pem server-cert.pem cert.pem
```

  
#### Iniciar Docker con TLS

Detenemos el servicio docker

```sh
sudo systemctl stop docker
```

Iniciamos el daemon Docker de forma manual:

```sh
sudo dockerd \
--tlsverify \
--tlscacert=ca.pem \
--tlscert=server-cert.pem \
--tlskey=server-key.pem \
-H=0.0.0.0:2376
```

#### En la maquina cliente remota
  

```sh
$ docker --tlsverify \
--tlscacert=ca.pem \
--tlscert=cert.pem \
--tlskey=key.pem \
-H=tcp://192.168.81.9:2376 version
```

```sh
$ export DOCKER_HOST=tcp://192.168.81.9:2376
$ export DOCKER_TLS_VERIFY=1 
# En mi Windows:
$ export DOCKER_CERT_PATH="C:\Users\mitch\Documents\docker-tls"
```

#### Prueba en maquina cliente Windows

```sh
$ docker ps
$ docker ps -a
```




### *Aplicar el manifiesto y validar*

Ahora aplico el archivo:

bash
kubectl apply -f rbac.yaml


> Esto crea el usuario, el rol y el binding en Kubernetes.

Verificamos que el usuario se haya creado:

bash
kubectl get serviceaccounts


Verificamos que el rol exista:

bash
kubectl get role exec-role


Verificamos el binding:

bash
kubectl get rolebinding exec-binding


---

### *Validación final del acceso*

Validamos si el usuario tiene permiso para ejecutar comandos en pods:

bash
kubectl auth can-i create pods/exec --as=system:serviceaccount:default:exec-user


> Si el resultado es yes, significa que nuestro RBAC fue aplicado correctamente.