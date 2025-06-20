# 🗳️ Real-Time Voting App on Kubernetes (Minikube)

This project deploys a real-time voting application using Kubernetes on Minikube. It demonstrates a microservice architecture with autoscaling enabled for the backend API using Horizontal Pod Autoscaler (HPA).

---

## 🧩 Architecture

```
+-----------+       +----------+       +--------+
| Frontend  | <---> | Backend  | <---> | Redis  |
+-----------+       +----------+       +--------+
                         |
                    +-----------+
                    | Autoscaler|
                    +-----------+
```

---

## ✅ Prerequisites

- Linux VM with at least 2 vCPUs (e.g. GCP `e2-standard-2`)
- Minikube and kubectl installed
- Docker installed for building/pushing images
- Optional: `hey` or `k6` for load testing

---

## 🏁 Setup Instructions

### 1. Start Minikube

```bash
minikube start
minikube addons enable metrics-server
```

---

### 2. Deploy Redis
- First upload the 3 folders, frontend, backend, and k8s to a storage bucket called _votingapp_
- Get your vm connected to Google Cloud Storage
- 1. Find the service account for your vm
- 2. Then run the following command in your google cloud console (not the vm console) to give your vm access to the cloud storage bucket

```bash
gcloud storage buckets add-iam-policy-binding gs://YOUR_BUCKET_NAME \
    --member="serviceAccount:MY_VM_SERVICE_ACCOUNT" \
    --role="roles/storage.objectViewer" # Or objectCreator, objectAdmin, etc.
```

- then copy over all of these files to your vm

```bash
gsutil cp -r gs://votingapp /home/YOUR_ACCOUNT/
```

```bash
kubectl apply -f votingapp/k8s/redis.yaml
```
---

### 3. Deploy Backend API

```bash
kubectl apply -f votingapp/k8s/backend.yaml
```

---

### 4. Deploy Frontend

```bash
kubectl apply -f votingapp/k8s/frontend.yaml
```

---

### 5. Enable Autoscaling

```bash
kubectl autoscale deployment backend --cpu-percent=50 --min=1 --max=5
kubectl get hpa
kubectl top pods
```

---

### 6. Build and Push Docker Images

Replace `your-dockerhub-username` with your Docker Hub username.

```bash
docker build -t your-dockerhub-username/backend:latest ./votingapp/backend
docker build -t your-dockerhub-username/frontend:latest ./votingapp/frontend

docker push your-dockerhub-username/backend:latest
docker push your-dockerhub-username/frontend:latest
```

---

### 7. Port-forward Frontend to Access

```bash
kubectl port-forward service/frontend 8080:80
```

Open your browser and visit:

```
http://localhost:8080
```

---

### 8. (Optional) Load Testing

Install `hey`:

```bash
go install github.com/rakyll/hey@latest
```

Run load test:

```bash
~/go/bin/hey -z 30s -c 10 http://backend:8080/vote
```

---

## 📦 Project Structure

```
.
├── backend/
├── frontend/
├── k8s/
└── README.md
```
