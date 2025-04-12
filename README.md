# Microservices Project – Final Deployment

A fully containerized, microservices-based system built with Flask and SQLite. Each service is designed to run independently and communicate using RESTful APIs. The project is deployed on a Kubernetes (Minikube) cluster with integrated monitoring via Prometheus and Grafana and centralized logging using Elasticsearch, Fluentd, and Kibana (EFK).

---

## 📚 Table of Contents
- Overview
- Architecture
- Tech Stack
- Features
- Getting Started
- Microservice Structure
- Deployment
- Monitoring & Logging
- CI/CD

---

##  Overview
This system simulates a food ordering and delivery platform with multiple services. Customers can browse a menu, place bookings, and confirm order pickups. Drivers are managed and assigned dynamically based on availability.

---

## 🛠️ Architecture
- **Microservices**: Admin, Menu, Booking, Confirm, Driver
- **Database**: Each service uses a local SQLite database
- **Communication**: REST APIs with Kubernetes DNS or NodePort access
- **Containerization**: Docker
- **Orchestration**: Kubernetes via Minikube
- **Monitoring**: Prometheus & Grafana
- **Logging**: Elasticsearch + Fluentd + Kibana (EFK)

---

## 📊 Tech Stack
| Component     | Tool / Framework       |
|--------------|------------------------|
| Language      | Python 3.11            |
| Framework     | Flask                  |
| Database      | SQLite                 |
| Container     | Docker                 |
| Orchestration | Kubernetes (Minikube)  |
| CI/CD         | GitHub Actions         |
| Monitoring    | Prometheus, Grafana    |
| Logging       | EFK Stack              |
| Testing       | pytest                 |

---

## 📅 Features
- Full CRUD APIs for all microservices
- Dynamic driver availability and auto assignment
- Confirm service with internal service calls
- RESTful architecture with internal DNS and external NodePort access
- Horizontal Pod Autoscaling (HPA) for `admin`
- CI/CD pipeline via GitHub Actions
- Centralized monitoring (Grafana)
- Centralized logging (EFK stack)
- Role-based access control and network policy enforcement

---

## ⚖️ Getting Started

### Prerequisites
- Python 3.11+
- Docker
- Minikube
- kubectl
- Helm

### Clone the Project
```bash
git clone <your-repo-url>
cd micro
```

---

## 🛋️ Microservice Structure
Each service follows the same design pattern:

```
├── app.py           # Entry point
├── models.py        # SQLAlchemy models
├── routes.py        # API routes
├── requirements.txt # Dependencies
├── Dockerfile       # Container configuration
├── tests/           # Unit and integration tests
```

---

## 🚀 Deployment

### Start Minikube
```bash
minikube start --cpus=4 --memory=8192
```

### Load Docker images into Minikube
```bash
eval $(minikube docker-env)
docker build -t micro-admin:latest ./admin
docker build -t micro-booking:latest ./booking
docker build -t micro-confirm:latest ./confirm
docker build -t micro-driver:latest ./driver
docker build -t micro-menu:latest ./menu
```

### Apply Kubernetes manifests
```bash
kubectl apply -f k8s/
```

---

## 📊 Monitoring & Logging

### Prometheus + Grafana (via Helm)
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
kubectl port-forward service/prometheus-grafana 3000:80
```

Access: [http://localhost:3000](http://localhost:3000)
User: `admin` / Password: `prom-operator`

### EFK Stack (via Helm)
```bash
helm install elasticsearch bitnami/elasticsearch
helm install fluentd bitnami/fluentd
helm install kibana bitnami/kibana --set elasticsearch.hosts[0]=elasticsearch.default.svc.cluster.local
kubectl port-forward svc/kibana 5601:5601
```

---

## 🛠️ CI/CD

### GitHub Actions
Workflow is defined in `.github/workflows/ci.yml`

**Flow:**
- Trigger: push to `main`
- Run `pytest` tests for all services
- Build Docker images for each microservice
- Optionally push images to Docker Hub or other registry

---

## ✨ Optional Enhancements
- Role-Based Access Control (RBAC)
- Network Policies (e.g., restrict `menu` -> `driver` access)
- Service Discovery using Kubernetes DNS
- Centralized logging dashboard using Kibana

---

This project demonstrates a complete modern DevOps-ready architecture built on microservices principles and designed for reliability, observability, and scalability.


