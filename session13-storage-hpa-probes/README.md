# Session 13 — Kubernetes Storage, HPA, and Probes

## Task 1 — Volumes

| Storage type | What it is | Practical use |
|---|---|---|
| `emptyDir` | Directory created with a Pod and deleted with it; containers in that Pod can share it. | Temporary cache and app-to-sidecar file sharing. |
| `hostPath` | Mounts a worker-node filesystem path. | Trusted node agents, such as log collectors; avoid for portable apps. |
| PersistentVolume (PV) | Cluster-level storage capacity supplied by an administrator or provisioner. | The durable storage resource. |
| PersistentVolumeClaim (PVC) | A workload request for storage capacity/access mode. | Apps mount the claim instead of storage-specific implementation. |
| StorageClass | Storage-provisioning policy. | Selects provisioner, parameters, and reclaim policy. |
| Dynamic provisioning | A PVC automatically causes its StorageClass provisioner to create a PV. | Default approach on Minikube and cloud Kubernetes. |

Example `emptyDir`:

```yaml
volumes: [{name: cache, emptyDir: {}}]
containers:
  - name: app
    volumeMounts: [{name: cache, mountPath: /cache}]
```

Example `hostPath`:

```yaml
volumes: [{name: host-logs, hostPath: {path: /var/log, type: Directory}}]
```

This session's mini project uses the default Minikube `standard` StorageClass. Its `web-content` PVC dynamically provisions and binds a 1Gi PV. The Deployment mounts that PVC; an init container creates `index.html` before NGINX starts so the HTTP readiness/liveness probes remain healthy.

## Task 2 — HPA hands-on

```powershell
kubectl apply -f 02-hpa/hpa.yml
kubectl apply -f 02-hpa/load-generator.yml
kubectl get hpa -w
kubectl get pods -w
kubectl top pods
kubectl describe hpa hpa-demo
```

Metrics Server is required for `kubectl top` and HPA CPU calculations. On Minikube: `minikube addons enable metrics-server`.

Expected behavior: CPU crosses 50% of the 100m request, the HPA increases replicas up to 5, and it scales down after load is removed.

**Actual evidence:** During execution on 7 October 2026, the load generator drove CPU to `491%` of request. HPA increased the deployment from one to five replicas.

![Actual HPA output](./screenshots/hpa-scaling.png)

## Task 3 — Mini project

```powershell
kubectl apply -f mini-project/pvc.yaml
kubectl apply -f mini-project/app.yaml
kubectl get pvc,pv,pods,svc
kubectl describe pvc web-content
```

The project demonstrates durable storage, a Service, and health probes. Capture `kubectl get hpa`, `kubectl top pods`, `kubectl describe hpa`, and `kubectl get pvc,pv,pods` in `screenshots/` after the cluster is running.

**Actual evidence:** The default `standard` StorageClass dynamically provisioned and bound a 1Gi PV for `web-content`. The first deployment surfaced an empty-volume/probe issue; an init container now initializes `index.html` before NGINX starts, and both replicas became Ready.

![Actual storage mini project](./screenshots/storage-mini-project.png)
