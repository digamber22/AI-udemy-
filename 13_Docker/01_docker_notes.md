# Docker Notes

## 1) What is Docker?

Docker is a platform used to **build, package, ship, and run applications** inside lightweight, isolated environments called **containers**.

It helps solve common deployment problems such as:

* "It works on my machine"
* dependency mismatch
* different runtime versions
* missing libraries
* hard-to-manage environment setup

Docker helps an application run the same way on different systems, as long as the Docker environment is supported.

---

## 2) What problem does Docker solve?

Before Docker, software often failed because it depended on a specific:

* operating system setup
* library version
* language runtime version
* configuration file
* system package

### Example

An app may run on one machine but fail on another because:

* Python version is different
* Node.js version is different
* a database client is missing
* OS libraries are missing

Docker solves this by bundling the app with everything it needs.

---

## 3) Possible solutions to deployment and environment problems

Different technologies can solve these issues in different ways:

### a) Manual setup

Install everything directly on the host machine.

**Problem:**

* hard to maintain
* environment mismatch
* conflicts between apps

### b) Virtualization

Run a full virtual machine with its own guest operating system.

**Problem solved:**

* strong isolation
* multiple OS environments on one machine

**Downside:**

* heavier
* slower to start
* uses more memory and disk
* includes a full OS for each VM

### c) Containers

Share the host OS kernel while isolating the application process.

**Benefits:**

* lightweight
* fast startup
* less memory usage
* easy to move and deploy

### d) Cloud or Platform-as-a-Service

Deploy directly to managed platforms.

**Benefit:**

* less infrastructure management

**Downside:**

* less control than containers or VMs

---

## 4) Why Docker is better than virtualization in many cases

Docker is usually more efficient than virtualization because it is **lightweight**.

### Virtual machine

A VM includes:

* hardware virtualization layer
* guest operating system
* application

This makes it heavier.

### Docker container

A container includes:

* application
* dependencies
* user-space libraries
* isolated process space

It **shares the host kernel** instead of running a full OS inside each container.

### Advantages of Docker over VMs

* uses less memory
* starts faster
* smaller size
* easier to scale
* more efficient for microservices
* better resource utilization

---

## 5) Important downside of Docker

Docker containers share the host kernel.

That means:

* Linux containers run on the Linux kernel
* Windows containers need Windows kernel support
* a container built for one OS family may not run directly on another OS family without compatibility support

### Practical meaning

A container is not a full machine.
It depends on the kernel of the host system or a compatible kernel layer.

So Docker is lightweight, but it is **less isolated than a full virtual machine**.

---

## 6) What is a container?

A container is a **running instance of an image**.

It is a lightweight isolated environment that runs a process.

### Simple idea

* **Image** = blueprint
* **Container** = running copy of that blueprint

A container includes:

* application code
* runtime
* libraries
* environment variables
* filesystem changes while running

---

## 7) Difference between Docker image and Docker container

### Docker image

A Docker image is a **read-only template** or blueprint.
It contains:

* app code
* dependencies
* base operating system layers
* startup instructions
* metadata

Think of it like a recipe.

### Docker container

A Docker container is a **running instance of an image**.
It is created from an image and can be started, stopped, killed, and removed.

Think of it like the cooked food made from the recipe.

### Main difference

* Image = static, stored, reusable
* Container = dynamic, running, live process

---

## 8) Docker commands

### `docker version`

Shows Docker version information.
It usually displays:

* client version
* server or engine version
* API version
* build details

Useful for checking whether Docker is installed properly.

---

### `docker run -it image_name`

Runs a new container from the image.

#### What `run` means

`docker run` does two things:

1. creates a container from the image
2. starts that container

#### What `-i` means

`-i` stands for **interactive**.
It keeps standard input open, so you can type commands into the container.

#### What `-t` means

`-t` stands for **TTY**.
It allocates a pseudo terminal so the container behaves like a real terminal session.

#### What `-it` means together

`-it` means:

* interact with the container
* get a terminal interface

This is commonly used when opening shells like `bash` inside a container.

Example:

```bash
docker run -it image_name
```

---

### `docker run -it --name container_name image_name`

Runs a new container and gives it a custom name.

#### `--name`

Sets a friendly name for the container.

Instead of using a random container ID, you can refer to the container by name:

```bash
docker start container_name
```

Example:

```bash
docker run -it --name container_name image_name
```

---

### Exiting a running container

Inside the container shell:

* `exit` or `Ctrl + D` usually stops the shell and ends the container process

Important note:

* if the main process stops, the container stops

---

### `cls`

Clears the screen in Windows Command Prompt.

For Linux or macOS terminals, the equivalent is usually:

```bash
clear
```

---

### `docker ps --help`

Shows help for the `docker ps` command.

---

### `docker ps`

Lists running containers only.

Shows details like:

* container ID
* image name
* command
* created time
* status
* ports
* name

---

### `docker ps -a`

Lists all containers:

* running containers
* stopped containers
* exited containers

Useful when you want to see old containers too.

---

### `docker images`

Shows all locally available Docker images.

It displays:

* repository name
* tag
* image ID
* creation time
* size

---

### `docker info`

Shows detailed information about the Docker setup, such as:

* number of containers
* number of images
* storage driver
* security options
* Docker root directory
* system resources

Useful for checking Docker engine status and system configuration.

---

### `docker pull image_name`

Downloads an image from a registry like Docker Hub.

Example:

```bash
docker pull image_name
```

#### Important

`pull` only downloads the image.
It does **not** start a container.

To run it, use `docker run`.

---

## 9) Docker image commands

### `docker image --help`

Shows help for image-related commands.

---

### `docker image inspect image_name`

Shows detailed low-level metadata of the image.

This may include:

* image ID
* layers
* creation date
* environment variables
* entrypoint
* command
* OS type
* architecture
* size

#### What `inspect` means

`inspect` gives structured internal details about an image or container.
It is useful when you want deep technical information.

Example:

```bash
docker image inspect image_name
```

---

### `docker image ls`

Lists local Docker images.

This is similar to:

```bash
docker images
```

Both are commonly used.

---

### `docker image prune`

Removes unused images.

Usually this removes **dangling images** or images not being used by any container.

#### Why use it?

* free disk space
* clean up old image layers

Be careful: deleted images may need to be pulled again later.

---

### `docker image rm image_name`

Removes a Docker image.

Example:

```bash
docker image rm image_name
```

#### Note

An image can be removed only if it is not being used by a container.
If a container depends on that image, Docker may block removal unless forced.

---

## 10) Docker container commands

### `docker kill container_id`

Forcibly stops a running container immediately.

This is like a hard stop.

It does **not** remove the container.

---

### `docker rm container_id`

Removes a container.

Important:

* `rm` removes the container itself
* it does **not** remove the image
* it usually works only when the container is stopped

Example:

```bash
docker rm container_id
```

---

### Difference between `kill` and `rm`

#### `docker kill`

* stops a running container
* container still exists after stopping

#### `docker rm`

* deletes the container
* container is removed from Docker

### Important correction

`docker rm` does **not** remove images.
It removes the container only.

---

## 11) Very short summary

* Docker solves environment and deployment consistency problems.
* It is lightweight because it shares the host kernel.
* Virtualization is heavier because each VM has a full OS.
* An image is the blueprint.
* A container is the running instance of that image.
* `docker run` creates and starts a container.
* `docker ps` shows running containers.
* `docker ps -a` shows all containers.
* `docker images` shows local images.
* `docker pull` downloads images.
* `docker image inspect` shows detailed image metadata.
* `docker image prune` removes unused images.
* `docker kill` stops a running container.
* `docker rm` removes a container.

---

## 12) Exam-friendly one-line definitions

**Docker:** A platform for building and running applications in containers.

**Container:** A lightweight isolated runtime environment.

**Image:** A read-only template used to create containers.

**Virtualization:** Running multiple full operating systems on a single physical machine.

**Kernel sharing:** Containers use the host kernel instead of shipping a full OS.
