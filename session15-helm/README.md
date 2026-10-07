# Session 15 — Helm

Helm packages Kubernetes templates into versioned charts. This repository includes a working chart at `charts/webapp`.

```powershell
# Commands and purpose
helm create demo-chart                 # scaffold a chart
helm lint charts/webapp                # validate chart conventions
helm template demo charts/webapp       # render locally
helm install web charts/webapp         # create release revision 1
helm list                              # list releases
helm status web                        # release health/details
helm get manifest web                  # rendered manifests of release
helm upgrade web charts/webapp --set replicaCount=3 --set image.tag=1.27.4-alpine
helm history web                       # revisions
helm rollback web 1                    # return to revision 1
helm uninstall web                     # remove release
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx
```

## Rollback workflow

Install (revision 1) → upgrade replicas/image (revision 2) → verify `kubectl get pods` → upgrade again (revision 3) → verify → `helm rollback web 1` → verify revision 4 uses revision-1 values.

## Mini project

The `webapp` chart parametrizes replica count, image, Service, and resources. Keep screenshots from `helm list`, `status`, `history`, and `kubectl get pods` in `screenshots/`.
