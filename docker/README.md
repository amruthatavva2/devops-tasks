# Docker Homework: Hello World Applications

This folder contains six separate Hello World web applications. Each application has its own code and Dockerfile, as required.

## Folder structure

```text
docker/
├── nodejs-app/
├── python-app/
├── java-app/
├── Apache-app/
├── React-app/
└── nginx-app/
```

## Applications and Docker commands

Run each pair of commands from inside its application folder. Then open the listed URL in a browser to verify that the Hello World message appears.

| Application folder | Build command | Run command | Verify in browser |
| --- | --- | --- | --- |
| `nodejs-app` | `docker build -t hello-nodejs .` | `docker run --rm -p 3000:3000 hello-nodejs` | `http://localhost:3000` |
| `python-app` | `docker build -t hello-python .` | `docker run --rm -p 5000:5000 hello-python` | `http://localhost:5000` |
| `java-app` | `docker build -t hello-java .` | `docker run --rm -p 8080:8080 hello-java` | `http://localhost:8080` |
| `Apache-app` | `docker build -t hello-apache .` | `docker run --rm -p 8081:80 hello-apache` | `http://localhost:8081` |
| `React-app` | `docker build -t hello-react .` | `docker run --rm -p 8082:80 hello-react` | `http://localhost:8082` |
| `nginx-app` | `docker build -t hello-nginx .` | `docker run --rm -p 8083:80 hello-nginx` | `http://localhost:8083` |

For example, to run the Node.js application:

```bash
cd nodejs-app
docker build -t hello-nodejs .
docker run --rm -p 3000:3000 hello-nodejs
```

Expected webpage text:

```text
Hello World from Node.js!
```

## What each Dockerfile does

- **Node.js:** starts a small Node HTTP server on port `3000`.
- **Python:** installs Flask and starts a Flask web app on port `5000`.
- **Java:** compiles `Main.java` and starts a built-in Java HTTP server on port `8080`.
- **Apache:** serves `index.html` using the Apache HTTP Server on port `80`.
- **React:** builds the React/Vite application in a Node build stage, then serves the production files with Nginx on port `80`.
- **Nginx:** serves `index.html` directly with Nginx on port `80`.



## Submission checklist

- [x] Created all six required application folders.
- [x] Added application source code and a Dockerfile for every application.
- [ ] Build and run each image on a computer with Docker installed.
- [ ] Take screenshots of all six Hello World webpages.
- [ ] Push the `docker` folder to the GitHub repository.
