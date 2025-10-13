# (Not Updated) Deployment of Flask app with PostgreSQL database within a Kubernetes cluster

(Yet to add)
- Deployment of Numaflow pipeline
- Deployment of Kafka brokers
- Deployment of consumer scripts

#

Installation of Numaflow on local cluster
```bash
kubectl create ns numaflow-system
kubectl apply -n numaflow-system -f https://raw.githubusercontent.com/numaproj/numaflow/main/config/install.yaml
kubectl apply -f https://raw.githubusercontent.com/numaproj/numaflow/main/examples/0-isbsvc-jetstream.yaml
```

Instantiating new k8s cluster using Kind
```bash
kind create cluster --name my-cluster --config manifests/kind-config.yaml
kind load docker-image keeyiahn/flask-app:latest --name my-cluster 
```
Applying manifest file to create Numaflow pipeline
```bash
kubectl apply -f manifests/test-pipeline.yaml
```

Applying manifest files for Flask app deployment, NodePort service to expose Flask app to external access
```bash
kubectl apply -f manifests/flask/flask-app-deployment.yaml
kubectl apply -f manifests/flaskflask-app-service.yaml
```

Applying manifest files to deploy PostgreSQL database; PVC for persistent data storage, Deployment to run PostgreSQL server, Cluster-IP service for intra-cluster communication between PostgreSQL server & Flask app 
```bash
kubectl apply -f manifests/postgres-db/postgres-secret.yaml
kubectl apply -f manifests/postgres-db/postgres-pvc.yaml
kubectl apply -f manifest/postgres-dbs/postgres-deployment.yaml
kubectl apply -f manifests/postgres-db/postgres-service.yaml
```
Default credentials:
```
  POSTGRES_USER: flaskuser
  POSTGRES_PASSWORD: flaskpass
  POSTGRES_DB: flaskdb
```
(can be changed in postgres-secret.yaml, remember to update flask-app.py credentials as well)

Enter PostgreSQL server to initialise users table
```bash
kubectl exec -it <postgre-pod> -- psql -U flaskuser -d flaskdb
```
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
```

