# Session 20 — Monitoring, Observability, and GitOps

## Monitoring demo

```powershell
kubectl apply -f monitoring/app.yaml
kubectl get pods -l app=observability-demo
kubectl top pods -l app=observability-demo
kubectl logs deploy/observability-demo
kubectl describe deployment observability-demo
```

Metrics show numeric CPU/memory/requests; logs record events/messages; alerts notify when a threshold or health condition is breached. Application health comes from readiness/liveness probes. `kubectl top` requires Metrics Server.

## Observability

The three pillars are **metrics** (time-series measurements), **logs** (discrete event records), and **traces** (a request path across services). Observability explains unknown failures using emitted system signals. Common tools: Prometheus/Grafana for metrics, Loki/ELK for logs, and Jaeger/Tempo/OpenTelemetry for traces. In Kubernetes, collect node/container metrics, API/workload events, application logs, and distributed trace context.

## GitOps

GitOps uses Git as the source of truth for declarative cluster configuration. A controller such as Argo CD continuously compares Git's desired state with the actual cluster and reconciles drift. The included `gitops/application.yaml` is an Argo CD Application that tracks this repository's monitoring manifest with automated sync, prune, and self-heal.

```powershell
# after installing Argo CD
kubectl apply -f gitops/application.yaml
kubectl get applications -n argocd
```

Capture metrics/logs/probe output and Argo CD sync state under `screenshots/` after running the demo.
