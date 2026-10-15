# Session 21 — ProjectPulse DevOps Capstone

ProjectPulse is an original SaaS-style delivery-board application. It demonstrates the journey from a React interface and FastAPI REST API through testing, containers, CI security gates, Terraform, Kubernetes, Helm, monitoring, and troubleshooting.

> The app is deliberately not a direct copy of the instructor's TaskBoard reference. ProjectPulse uses its own domain, UI, API structure, naming, documentation, and implementation.

## Architecture

```text
React/Vite + Nginx ── /api ──> FastAPI + SQLAlchemy ──> PostgreSQL
       │                           │
       └── GitHub Actions: pytest → build → Trivy → optional GHCR/deploy
                                   │
                  Terraform AWS VPC + EKS → Helm → Ingress/HPA → Prometheus/Grafana
```

## Delivered requirements

| Area | Implementation |
| --- | --- |
| Application | Responsive ProjectPulse dashboard, create-task modal, filters, loading/error state |
| API | `GET /api/tasks`, `GET /api/tasks/{id}`, `POST`, `PUT`, `DELETE`, stats, health, ready, metrics |
| Database | PostgreSQL through SQLAlchemy; Alembic migration in `backend/alembic/versions/` |
| Tests | Six isolated pytest cases against SQLite test DB |
| Containers | Non-root Python image; multi-stage Node-to-unprivileged-Nginx frontend image; Compose stack |
| CI/DevSecOps | GitHub Actions test/build workflow with two Trivy HIGH/CRITICAL gates |
| IaC | AWS VPC, two public subnets, IGW/routes, EKS control plane, and managed node group |
| Kubernetes | Namespace, Helm chart, 2 frontend/2 backend replicas, services, Ingress, HPA, probes, PVC |
| Observability | Prometheus `/metrics`, optional ServiceMonitor, Grafana/Prometheus values |
| Troubleshooting | Deliberately invalid image and Service selector manifests |

## Run locally

Prerequisite: Docker Desktop running.

```powershell
cd session21-devops-capstone-final
docker compose up --build
```

Open <http://localhost:3000>. The direct API documentation is <http://localhost:8000/docs>; health is <http://localhost:8000/health>; Prometheus metrics are <http://localhost:8000/metrics>.

### Actual local verification evidence

The Compose stack was built and run locally on 15 October 2026. PostgreSQL became healthy, the backend returned `/health` and database-checking `/ready`, and the task statistics endpoint returned data from the live stack.

![Docker Compose and API health output](./screenshots/local-compose-api-health.png)

```powershell
docker compose down        # stop
docker compose down -v     # stop and delete local database data
```

## Test locally

Python 3.12 is recommended (the workstation currently has Python 3.10; containers/CI use 3.12).

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

Tests use a separate SQLite test database and never your Compose PostgreSQL database.

## Kubernetes and Helm

Build images locally first, then deploy to a Docker Desktop/Minikube cluster:

```powershell
kubectl apply -f k8s/namespace.yaml
helm upgrade --install projectpulse ./helm/taskboard -n projectpulse -f helm/taskboard/values-dev.yaml
kubectl get pods,svc,hpa -n projectpulse
helm list -n projectpulse
```

An Ingress controller and Metrics Server are needed for Ingress and HPA behavior. The dev hostname is `taskboard.local`; map it to your ingress IP in your hosts file. Enable monitoring after installing kube-prometheus-stack:

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f monitoring/prometheus-values.yaml
```

## Terraform: real AWS only

`terraform/` deliberately targets real AWS because EKS cannot be realistically emulated locally. It creates billable resources. You need an AWS account, AWS CLI credentials with VPC/EKS/IAM permissions, and a spending budget before using it.

```powershell
cd terraform
Copy-Item terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
# use the configure_kubectl output
terraform destroy
```

Never commit `terraform.tfvars`, `terraform.tfstate`, or access keys. Run `destroy` when finished.

## CI/CD and GHCR

The workflow runs pytest, builds the frontend, builds both images, and scans both images with Trivy. It fails on HIGH/CRITICAL vulnerabilities. On every push to `main`, the `publish-ghcr` job signs in with the repository's built-in `GITHUB_TOKEN` and publishes backend and frontend images to GHCR using the exact commit SHA. The non-enabled deploy job documents the Helm release command; enable it only after configuring Kubernetes authentication.

## Troubleshooting lab

```powershell
kubectl apply -f troubleshooting/broken-image.yaml
kubectl get pods -n projectpulse
kubectl describe pod -n projectpulse <pod-name>
kubectl get events -n projectpulse --sort-by=.lastTimestamp

kubectl apply -f troubleshooting/broken-service.yaml
kubectl get endpoints -n projectpulse broken-selector
kubectl get pods -n projectpulse --show-labels
```

`broken-image.yaml` demonstrates `ImagePullBackOff`; fix its image/tag. `broken-service.yaml` selects no Pods; correct the selector to `app: projectpulse-backend` and verify endpoints appear.

## What you need to install or create

Already available: Docker Desktop, Node, Helm, kubectl, and Terraform. Install Python 3.12 if you want to execute backend tests directly instead of through the CI/container runtime.

Optional/required only for the real cloud sections:

- AWS account and configured AWS CLI: Terraform VPC/EKS deployment; this may incur charges.
- GitHub Actions/GHCR: repository package permissions for image publication.
- A Kubernetes cluster plus NGINX Ingress Controller, Metrics Server, and kube-prometheus-stack: live Helm/HPA/Prometheus/Grafana demonstration.

## Submission checklist

- [x] Application source, API, migration, tests, Dockerfiles, Compose, CI workflow, security scans, Terraform, Helm, monitoring config, troubleshooting manifests, documentation
- [ ] Capture live Docker browser/Compose/test evidence
- [ ] Enable GHCR push and capture a successful Actions run
- [ ] Provision and destroy real AWS EKS only if you have approved AWS billing
- [ ] Capture live Kubernetes, Prometheus, and Grafana evidence from a configured cluster
