# 🗳️ Real-Time Voting App on Kubernetes

This project deploys a real-time voting application using Kubernetes. It demonstrates a microservice architecture with autoscaling enabled for the backend API using Horizontal Pod Autoscaler (HPA).

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

- GKE cluster created
- Docker installed for building/pushing images
- Optional: `hey` or `k6` for load testing

---

## 🏁 Setup Instructions

- go to your frontend and backend yaml files in the k8s folder
- change where it says yourdockerusename to yourdockerusername
- spec:
      containers:
      - name: backend
        image: yourdockerusername/backend:latest

### 1. Open your Cloud Console

```bash
gcloud config list
gcloud container clusters get-credentials votingapp --region YOUR_CLUSTER_REGION --project YOUR_PROJECT_ID
```

---

### 2. Deploy Redis
- 1. Make sure you uploaded the 3 folders, frontend, backend, and k8s to a storage bucket called _votingapp_
- 2. Then run the following command in your google cloud console (not the vm console) to give your vm access to the cloud storage bucket

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
kubectl get service frontend -n default
```

Open your browser and visit:

```
http://<EXTERNAL_IP>
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
