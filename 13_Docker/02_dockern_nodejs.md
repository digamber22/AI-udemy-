# Docker Guide for Node.js: From Development to Production

This note covers how to create and use a Dockerfile for a Node.js app, how to build and run images, port mapping, environment variables, pushing images, custom Dockerfiles, and a production-ready multi-stage build.

---

## 1) What Docker does

Docker packages your application and everything it needs into an **image**.
A running instance of an image is called a **container**.

* **Image**: the blueprint or template.
* **Container**: a running process created from an image.
* **Dockerfile**: a text file with instructions to build an image.

---

## 2) Creating a Dockerfile for a Node.js app

A Dockerfile tells Docker how to build your app image.

### Basic example

```dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8000
CMD ["npm", "start"]
```

### Meaning of each instruction

* **FROM node:20**
  Uses the official Node.js version 20 base image.

* **WORKDIR /app**
  Sets `/app` as the working directory inside the container.

* **COPY package*.json ./**
  Copies `package.json` and `package-lock.json` first. This helps Docker reuse cached layers when source code changes but dependencies do not.

* **RUN npm install**
  Installs dependencies inside the image.

* **COPY . .**
  Copies the rest of the application files into the container.

* **EXPOSE 8000**
  Documents that the container listens on port `8000`. It does not publish the port by itself.

* **CMD ["npm", "start"]**
  Runs the app when the container starts.

---

## 3) Build the image

```bash
docker build -t my-app .
```

### Meaning

* **docker build**: builds an image from a Dockerfile.
* **-t my-app**: tags the image with the name `my-app`.
* **.**: build context, meaning the current folder.

---

## 4) Run the container

### Map one port

```bash
docker run -it -p 3000:8000 my-app
```

### Meaning

* **docker run**: creates and starts a container.
* **-i**: keeps STDIN open.
* **-t**: gives a terminal-like interface.
* **-p 3000:8000**: maps port `3000` on your host machine to port `8000` inside the container.
* **my-app**: image name.

So if your Node app listens on port `8000` inside the container, you can open it from your machine at `http://localhost:3000`.

### Detached mode

```bash
docker run -itd -P --rm my-app
```

### Meaning

* **-d**: detached mode, runs the container in the background.
* **-P**: publishes all exposed ports to random available ports on the host.
* **--rm**: removes the container automatically when it stops.

### Important note

* `-p` = manual port mapping
* `-P` = automatic port mapping for all exposed ports

---

## 5) Dockerfile and multiple exposed ports

You can expose more than one port by writing multiple `EXPOSE` lines.

```dockerfile
EXPOSE 8000
EXPOSE 3001
```

With `-P`, Docker maps all exposed ports automatically.

---

## 6) Environment variables

Node apps often need environment variables like `PORT`, `NODE_ENV`, or database values.

### Pass variables directly

```bash
docker run -it -p 3000:3000 -e PORT=3000 -e x=y my-app
```

### Meaning

* **-e PORT=3000**: sets the environment variable `PORT` inside the container.
* **-e x=y**: sets another environment variable `x`.

### Load variables from a file

```bash
docker run -it -p 3000:3000 --env-file=./.env my-app
```

### Meaning

* **--env-file=./.env**: loads environment variables from a `.env` file.

Example `.env` file:

```env
PORT=3000
NODE_ENV=production
DB_HOST=localhost
```

---

## 7) Tagging and publishing an image

### Tag an image

```bash
docker tag my-app digamber/node-application:v1
```

### Meaning

* **docker tag**: gives an existing image a new name or version.
* **digamber/node-application**: repository name on Docker Hub.
* **v1**: version tag.

If you do not add a tag, Docker uses `latest` by default.

### Push the image

```bash
docker push digamber/node-application:v1
```

Before pushing, you usually need to log in:

```bash
docker login
```

---

## 8) Using a custom Dockerfile name

Sometimes you have more than one Dockerfile.

```bash
docker build -t ts-app-old -f Dockerfile.old .
```

### Meaning

* **-f Dockerfile.old**: tells Docker to use `Dockerfile.old` instead of the default `Dockerfile`.
* **ts-app-old**: image name.
* **.**: build context.

This is useful when you want different builds for development, testing, or production.

---

## 9) Production-ready multi-stage Docker build

A multi-stage build helps create a smaller and cleaner production image.

### Why use it?

* reduces final image size
* excludes unnecessary development files
* improves security
* keeps production image lean

### Example

```dockerfile
# Stage 1: Build stage
FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production stage
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY --from=builder /app/dist ./dist

EXPOSE 8000
CMD ["node", "dist/index.js"]
```

### Step-by-step explanation

#### Stage 1: builder

* **FROM node:20 AS builder**
  Creates a first stage named `builder`.

* **RUN npm install**
  Installs all dependencies, including dev dependencies.

* **RUN npm run build**
  Builds the app, for example compiling TypeScript into JavaScript.

#### Stage 2: production

* **FROM node:20-alpine**
  Uses a smaller Alpine Linux-based Node image.

* **RUN npm install --omit=dev**
  Installs only production dependencies.

* **COPY --from=builder /app/dist ./dist**
  Copies only the built output from the builder stage.

* **CMD ["node", "dist/index.js"]**
  Starts the production app.

---

## 10) Running as a non-root user

For better security, avoid running the app as root inside the container.

### Example

```dockerfile
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodeuser

USER nodeuser
```

### Meaning

* **addgroup --system**: creates a system group.
* **--gid 1001**: sets the group ID.
* **adduser --system**: creates a system user.
* **--uid 1001**: sets the user ID.
* **USER nodeuser**: runs the container as that user instead of root.

### Why this matters

Running as a non-root user is safer because the app gets fewer permissions.

---

## 11) Useful command summary

```bash
# Build image
docker build -t my-app .

# Run with port mapping
docker run -it -p 3000:8000 my-app

# Run in background and remove on stop
docker run -itd -P --rm my-app

# Pass environment variables
docker run -it -p 3000:3000 -e PORT=3000 -e x=y my-app

# Load env file
docker run -it -p 3000:3000 --env-file=./.env my-app

# Tag image
docker tag my-app digamber/node-application:v1

# Push image
docker push digamber/node-application:v1

# Build using another Dockerfile
docker build -t ts-app-old -f Dockerfile.old .
```

---

## 12) Very short memory version

* **Build**: `docker build -t my-app .`
* **Run**: `docker run -it -p host:container my-app`
* **Auto port mapping**: `-P`
* **Background mode**: `-d`
* **Auto remove**: `--rm`
* **Env variables**: `-e` or `--env-file`
* **Publish image**: `docker tag` then `docker push`
* **Custom Dockerfile**: `-f Dockerfile.name`
* **Production best practice**: use a multi-stage build and a non-root user

---

## 13) Final production checklist

Before deploying a Node.js container:

* use a small base image
* install only needed dependencies
* use multi-stage builds
* expose only required ports
* set environment variables properly
* run as a non-root user
* keep the image versioned with tags

---

If you use this as a GitHub note, the most important idea is simple: **Dockerfile defines the image, `docker build` creates it, and `docker run` starts the container.**
