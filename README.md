# Getting Started

Instantiating new k8s cluster using Kind
```bash
kind create cluster --name my-cluster --config manifests/kind-config.yaml
docker build -t keeyiahn/flask-app:latest .
kind load docker-image keeyiahn/flask-app:latest --name my-cluster 
```

Applying manifest files for Flask app deployment, NodePort service to expose Flask app to external access
```bash
kubectl apply -f manifests/flask-app-deployment.yaml
kubectl apply -f manifests/flask-app-service.yaml
```

