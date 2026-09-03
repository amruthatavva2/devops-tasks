# Docker Networking & Volume Homework

## Task 1: Container networking

This exercise creates three containers—frontend, backend, and database—and three isolated user-defined bridge networks. The backend is attached to both the frontend and backend networks, allowing it to communicate with both sides.

```text
frontend ── frontend-network ── backend ── backend-network ── database
                                      │
                                      └── backend-network

database ── database-network
```

## Task 2: Host network

An Apache HTTP Server container will be started with Docker host networking and tested at `http://localhost:80`.

## Task 3: Bind mount

The local [`bind-mount-site`](bind-mount-site) folder is mounted read-only into an Nginx container at `/usr/share/nginx/html`. The initial page says **Hello students**. I will update the local file and verify that Nginx serves the new version without restarting.

## Task 4: Overlay networks—research notes

An overlay network is a Docker network driver for connecting containers running on different Docker hosts in a Docker Swarm. It creates a virtual network above the physical network, so services can communicate using service names even when their tasks run on separate swarm nodes.

- **Use cases:** distributed microservices, multi-host application stacks, and Docker Swarm service discovery.
- **How it works:** the swarm manager distributes network configuration, Docker assigns virtual IP addresses and DNS service names, and data-plane traffic is encapsulated between hosts (VXLAN). Docker can encrypt overlay data traffic with `--opt encrypted`.
- **Requirement:** initialize or join a Docker Swarm, then create it with a command such as `docker network create --driver overlay app-overlay`. A regular single-host Docker Desktop setup cannot fully demonstrate cross-host overlay communication.

Actual commands, output, and verification evidence will be added below after the containers are running.

## Task 1 evidence: container networking

### Commands executed

```powershell
docker network create homework-frontend-network
docker network create homework-backend-network
docker network create homework-database-network

docker run -d --name networking-frontend --network homework-frontend-network -p 8084:80 nginx:1.27-alpine
docker run -d --name networking-backend --network homework-frontend-network alpine:3.20 sh -c "while true; do sleep 3600; done"
docker network connect homework-backend-network networking-backend
docker run -d --name networking-database --network homework-backend-network mysql:8.4
docker network connect homework-database-network networking-database
```

### Actual network and container output

```text
NAME                        DRIVER    SCOPE
homework-backend-network    bridge    local
homework-database-network   bridge    local
homework-frontend-network   bridge    local

Backend network attachments:
homework-backend-network homework-frontend-network

NAMES                 IMAGE               NETWORKS
networking-database   mysql:8.4           homework-backend-network,homework-database-network
networking-backend    alpine:3.20         homework-backend-network,homework-frontend-network
networking-frontend   nginx:1.27-alpine   homework-frontend-network
```

### Actual connectivity checks

```powershell
docker exec networking-frontend getent hosts networking-backend
docker exec networking-backend ping -c 1 networking-database
```

```text
Frontend resolved backend:
172.18.0.3        networking-backend  networking-backend

Backend reached database:
PING networking-database (172.19.0.3): 56 data bytes
64 bytes from 172.19.0.3: seq=0 ttl=64 time=0.235 ms

1 packets transmitted, 1 packets received, 0% packet loss
```

I confirmed that Docker DNS resolves a container by its name on a shared user-defined network. The backend can reach both the frontend side and database side because it is attached to two networks.

## Task 2 evidence: Apache host network

### Command executed

```powershell
docker run -d --name networking-apache-host --network host httpd:2.4-alpine
docker ps --filter name=networking-apache-host
curl.exe http://localhost:80/
```

### Actual output

```text
NAMES                    IMAGE              NETWORKS   STATUS
networking-apache-host   httpd:2.4-alpine   host       Up

curl: (7) Failed to connect to localhost:80: Could not connect to server
```

The Apache container was created on Docker's `host` network, as shown by `docker ps`. However, Docker Desktop's optional **host networking** feature is disabled on this Windows computer, so host port `80` was not reachable. To complete this part on Docker Desktop, enable **Settings → Resources → Network → Enable host networking**, apply the change, restart Docker Desktop, then rerun the Apache container and open `http://localhost:80`.

> Docker's host network behaves differently on Docker Desktop than it does on native Linux. On native Linux, a host-network container shares the host network namespace directly and Apache normally becomes available on port `80` without `-p`.

## Task 3 evidence: bind mount

### Commands executed

```powershell
docker run -d --name networking-bind-nginx -p 8085:80 --mount "type=bind,src=<local-path>\bind-mount-site,dst=/usr/share/nginx/html,readonly" nginx:1.27-alpine
curl.exe http://localhost:8085/
```

### Initial webpage output

```html
<body><h1>Hello students</h1></body>
```

I then modified the local [`bind-mount-site/index.html`](bind-mount-site/index.html) file. I did not restart the Nginx container.

### Updated webpage output without restart

```html
<body><h1>Hello students - bind mount updated successfully</h1></body>
```

```text
NAMES                   PORTS                                     STATUS
networking-bind-nginx   0.0.0.0:8085->80/tcp, [::]:8085->80/tcp   Up
```

This proves that a bind mount maps the host folder into the container: changing the host file immediately changed the page served by Nginx at [http://localhost:8085](http://localhost:8085), without rebuilding or restarting the container.

## Submission checklist

- [x] Created frontend, backend, and database containers.
- [x] Created three Docker networks and attached the backend to two.
- [x] Verified frontend-to-backend and backend-to-database connectivity.
- [x] Pulled Apache and created a container with the host network.
- [x] Completed and verified the bind-mount exercise with a live file update.
- [x] Documented overlay-network concepts and multi-host use cases.
