# DevOps Homework Portfolio

This repository contains my completed DevOps homework tasks. Each topic has its own folder and its own README with commands, explanations, and practice output.

## Completed work

| Topic | Folder | What I completed |
| --- | --- | --- |
| Linux | [linux](linux) | Soft and hard links, `adduser` vs `useradd`, `journalctl`, and an essential Linux command cheat sheet. |
| Shell scripting | [shell-scripting](shell-scripting) | A Bash system-information script using variables, `read -p`, `mkdir`, `touch`, `df`, `ps`, and output redirection. |
| Networking | [networking](networking) | IP-addressing notes, networking-command explanations, and captured command outputs. |
| Git and GitHub | [git-github](git-github) | `git commit -m` vs `git commit -a -m`, branches, commit history, and a successful cherry-pick exercise. |
| Docker Hello World applications | [docker](docker) | Separate Node.js, Python, Java, Apache, React, and Nginx applications, each with source code and a Dockerfile. |
| Docker multi-stage build | [docker-multistage](docker-multistage) | A two-stage Node.js Docker build, verified on port `8080`, plus Node.js, Python, and Java Docker deployments. |
| Docker networking and volumes | [docker-networking-volume](docker-networking-volume) | Three-container networking, bind mounts with live updates, Apache host networking, and overlay-network research. |

## Main skills practiced

- Linux files, links, permissions, users, services, logs, and command-line tools.
- Bash scripting, variables, user input, directories, files, processes, and redirection.
- Networking concepts including IP addresses, routes, DNS, ports, connectivity, and Docker networks.
- Git commits, staging, branches, logs, and cherry-picking.
- Docker images, containers, Dockerfiles, multi-stage builds, port publishing, bind mounts, networks, and container-to-container communication.

## Docker verification summary

I installed and started Docker Desktop, built all six Hello World images, and ran/verified these applications with real HTTP responses:

| Application | URL | Result |
| --- | --- | --- |
| Node.js | `http://localhost:3000` | Hello World page verified |
| Python | `http://localhost:5000` | Hello World page verified |
| Java | `http://localhost:8081` | Hello World page verified |
| Multi-stage Node.js | `http://localhost:8080` | `Hello World from Docker multi-stage build` verified |
| Bind-mounted Nginx | `http://localhost:8085` | Local file update was reflected without restarting the container |

The Docker networking exercise also verified frontend-to-backend name resolution and backend-to-MySQL connectivity.



## Submission notes

- Each homework folder contains an individual README that can be submitted independently when required.

