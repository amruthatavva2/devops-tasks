$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& "$root\scripts\Capture-Command.ps1" 'minikube version; kubectl version --client' "$PSScriptRoot\..\screenshots\01-version-check.png" 'Session 9 — Version Checks'
& "$root\scripts\Capture-Command.ps1" 'minikube start' "$PSScriptRoot\..\screenshots\02-minikube-start.png" 'Session 9 — Minikube Start'
& "$root\scripts\Capture-Command.ps1" 'minikube status; kubectl get nodes -o wide' "$PSScriptRoot\..\screenshots\03-minikube-status-and-node.png" 'Session 9 — Cluster Health'
& "$root\scripts\Capture-Command.ps1" 'minikube stop; minikube status' "$PSScriptRoot\..\screenshots\04-minikube-stop.png" 'Session 9 — Minikube Stop'
