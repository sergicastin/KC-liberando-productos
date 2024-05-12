# Practica Liberando Productos - SRE

## Objetivo

El objetivo es mejorar un proyecto creado previamente para ponerlo en producción, a través de la adicción de una serie de mejoras.

## Proyecto inicial

El proyecto inicial es un servidor que realiza lo siguiente:

- Utiliza [FastAPI](https://fastapi.tiangolo.com/) para levantar un servidor en el puerto `8081` e implementa inicialmente dos endpoints:
  - `/`: Devuelve en formato `JSON` como respuesta `{"health": "ok"}` y un status code 200.
  - `/health`: Devuelve en formato `JSON` como respuesta `{"message":"Hello World"}` y un status code 200.

- Se han implementado tests unitarios para el servidor [FastAPI](https://fastapi.tiangolo.com/)

- Utiliza [prometheus-client](https://github.com/prometheus/client_python) para arrancar un servidor de métricas en el puerto `8000` y poder registrar métricas, siendo inicialmente las siguientes:
  - `Counter('server_requests_total', 'Total number of requests to this webserver')`: Contador que se incrementará cada vez que se haga una llamada a alguno de los endpoints implementados por el servidor (inicialmente `/` y `/health`)
  - `Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/health`.
  - `Counter('main_requests_total', 'Total number of requests to main endpoint')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/`.

## Instrucciones

1. Se almacena el webhook de Slack en una variable de entorno del sistema para poder editarlo fácilmente.

```sh
echo "export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/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'" >> ~/.bashrc
source ~/.bashrc
```

Comprobar que se ha almacenado correctamente haciendo un echo de la variable:

```sh
echo $SLACK_WEBHOOK_URL
```

2. Crear un clúster de kubernetes

```sh
minikube start --kubernetes-version='v1.28.3' \
    --cpus=4 \
    --memory=4096 \
    --addons="metrics-server,default-storageclass,storage-provisioner" \
    -p monitoring-demo
```

3. Añadir el repositorio de helm prometheus-community para poder desplegar el chart kube-prometheus-stack

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

4. Desplegar el chart kube-prometheus-stack del repositorio de helm añadido en el paso anterior con los valores configurados en el archivo kube-prometheus-stack/values.yaml en el namespace monitoring:

```sh
helm -n monitoring upgrade \
    --install prometheus \
    prometheus-community/kube-prometheus-stack \
    -f kube-prometheus-stack/values.yaml \
    --create-namespace \
    --wait --version 55.4.0
```

5. Añadir el repositorio de helm de mongodb para poder desplegar el operador de base de datos de mongodb.

```sh
helm repo add mongodb https://mongodb.github.io/helm-charts
helm repo update
```

6. Desplegar el helm chart del operador de mongodb.

```sh
helm upgrade --install community-operator \
    mongodb/community-operator \
    -n mongodb --create-namespace \
    --wait --version 0.9.0
```

7. Desplegar el helm chart con la aplicación fastApi

```sh
helm -n fast-api upgrade my-app --wait --install --create-namespace fast-api-webapp
```

8. Realizar un port-forward del puerto 8081 para la aplicación FastApi

```sh
kubectl -n fast-api port-forward svc/my-app-fast-api-webapp 8081:8081
```

9. Realizar un port-forward del puerto 8000 para las métricas

```sh
kubectl -n fast-api port-forward svc/my-app-fast-api-webapp 8000:8000
```

10. Realizar un port-forward del puerto 3000 para grafana

```sh
kubectl -n monitoring port-forward svc/prometheus-grafana 3000:http-web
```

11. Realizar un port-forward del puerto 9090 para prometheus

```sh
kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```

## Vídeo
Vídeo de la comprobación de mi práctica:
[Video](https://youtu.be/iyVvl4CT_QI?si=wabH8x_GMlTXLkOl)