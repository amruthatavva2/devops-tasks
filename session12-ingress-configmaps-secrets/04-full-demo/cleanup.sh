#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
kubectl delete -f "$here/ingress.yaml" --ignore-not-found
kubectl delete -f "$here/frontend.yaml" --ignore-not-found
kubectl delete -f "$here/backend.yaml" --ignore-not-found
kubectl delete -f "$here/secret.yaml" --ignore-not-found
kubectl delete -f "$here/configmap.yaml" --ignore-not-found
