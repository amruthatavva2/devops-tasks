# Kubernetes Volumes

| Type | Lifetime / location | Use case |
|---|---|---|
| `emptyDir` | Created with a Pod; deleted with that Pod | Shared scratch space, cache, sidecar hand-off |
| `hostPath` | A path on the worker node | Node agents only; avoid for portable apps |
| PersistentVolume (PV) | Cluster storage resource | Administrator-provided storage capacity |
| PersistentVolumeClaim (PVC) | Application request for PV capacity | Decouples application from storage details |
| StorageClass | Provisioning policy | Defines provisioner, reclaim policy, parameters |
| Dynamic provisioning | PVC triggers automatic PV creation | Standard approach for cloud/local CSI storage |

## Practical examples

`emptyDir` shares temporary files between containers:

```yaml
volumes: [{name: cache, emptyDir: {}}]
containers:
  - name: app
    volumeMounts: [{name: cache, mountPath: /cache}]
```

`hostPath` mounts a node directory (only use for trusted node-level workloads):

```yaml
volumes: [{name: host-logs, hostPath: {path: /var/log, type: Directory}}]
```

For dynamic provisioning, apply the PVC in `../mini-project/pvc.yaml`, then inspect:

```powershell
kubectl apply -f ../mini-project/pvc.yaml
kubectl get storageclass,pv,pvc
kubectl describe pvc web-content
```

The default Minikube StorageClass dynamically creates a backing PV after a PVC is requested. A PVC is the stable contract used by the application; a Pod can be replaced without losing data while the PVC remains bound.
