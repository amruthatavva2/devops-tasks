# Docker Multi-Stage Build Homework

## Student details

- **Name:** _Amrutha Tavva_
- **Enrollment number:** _24bcs10186_

## Task 1: Multi-stage Docker application

I used the multi-stage Dockerfile pattern from the Docker material in the shared `devops-heros` repository. The source is in [`multi-stage-app`](multi-stage-app). Its Dockerfile has two stages: `builder` installs dependencies, and `production` copies only runtime files and installs production dependencies.

### Commands executed

```powershell
cd docker-multistage
docker build -t hello-multistage .\multi-stage-app
docker run -d --name homework-multistage -p 8080:8080 hello-multistage
curl.exe http://localhost:8080/
docker ps --filter name=homework-multistage
```

### Actual application output

```html
<h1>Hello World from Docker multi-stage build</h1>
```

### Actual `docker ps` output

```text
NAMES                 IMAGE              PORTS                                         STATUS
homework-multistage   hello-multistage   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   Up About a minute
```

This confirms that the application runs on host port `8080`: [http://localhost:8080](http://localhost:8080).

## Task 3: Docker application deployment

I deployed and verified three different application types:

| Application | Image | URL | Actual output |
| --- | --- | --- | --- |
| Node.js | `hello-nodejs` | `http://localhost:3000` | `<h1>Hello World from Node.js!</h1>` |
| Python / Flask | `hello-python` | `http://localhost:5000` | `<h1>Hello World from Python!</h1>` |
| Java | `hello-java` | `http://localhost:8081` | `<h1>Hello World from Java!</h1>` |

### Commands and actual output

```powershell
docker run -d --name homework-nodejs -p 3000:3000 hello-nodejs
docker run -d --name homework-python -p 5000:5000 hello-python
docker run -d --name homework-java -p 8081:8080 hello-java

curl.exe http://localhost:3000/
curl.exe http://localhost:5000/
curl.exe http://localhost:8081/
docker ps --filter "name=homework-"
```

```text
--- NODE.JS ---
<h1>Hello World from Node.js!</h1>
--- PYTHON ---
<h1>Hello World from Python!</h1>
--- JAVA ---
<h1>Hello World from Java!</h1>

NAMES                 IMAGE              PORTS                                         STATUS
homework-java         hello-java         0.0.0.0:8081->8080/tcp, [::]:8081->8080/tcp   Up
homework-python       hello-python       0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   Up
homework-nodejs       hello-nodejs       0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   Up
homework-multistage   hello-multistage   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   Up
```

## Submission checklist

- [x] Built and ran the multi-stage Docker image.
- [x] Verified the required output and port `8080` mapping.
- [x] Deployed Node.js, Python, and Java applications.

