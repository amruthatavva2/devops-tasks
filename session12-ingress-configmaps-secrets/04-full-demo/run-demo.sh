#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
kubectl apply -f "$here/configmap.yaml"
kubectl apply -f "$here/secret.yaml"
kubectl apply -f "$here/backend.yaml"
kubectl apply -f "$here/frontend.yaml"
kubectl apply -f "$here/ingress.yaml"
kubectl rollout status deployment/yatri-backend
kubectl rollout status deployment/yatri-frontend
