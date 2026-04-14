# Docker Networking Notes

This note explains Docker bridge networking, why it is needed, how containers communicate, and the main Docker network drivers.

---

## 1) What is Docker networking?

Docker networking is the system that lets containers connect to each other, to the host machine, and to external networks.

Without networking, containers would be isolated and would not be able to talk to each other or expose services.

---

## 2) What is a bridge network?

A **bridge network** is a private internal network created on the Docker host. Containers attached to the same bridge can communicate with each other using their IP addresses or container names.

Think of it like a virtual switch inside your computer.

### Why it is needed

Bridge networking is used when:

* two or more containers need to communicate
* a container must connect to a database container
* you want network isolation from other containers
* you want the host to control how traffic enters and leaves containers

### Simple idea

If `container_one` and `container_two` are on the same bridge network, they can ping each other and exchange data.

---

## 3) Why read Docker networking?

You should understand Docker networking because most real apps are not just one container.

Examples:

* a Node.js app + MongoDB
* frontend + backend + database
* API container talking to Redis
* microservices talking to each other

Networking is what makes multi-container apps work.

---

## 4) Docker network drivers

Docker supports different network drivers. A **network driver** decides how containers connect.

### Common drivers

* **bridge**: default for standalone containers on one host
* **host**: container shares the host’s network directly
* **overlay**: used for containers across multiple Docker hosts, mostly in Swarm
* **macvlan**: gives containers their own MAC address on the physical network
* **ipvlan**: similar to macvlan, but uses IP-based networking
* **none**: disables networking for the container

---

## 5) Check Docker networks

```bash
docker network ls
```

### Meaning

* **docker network ls**: lists all Docker networks available on your machine.

Typical networks you may see:

* `bridge`
* `host`
* `none`

These are the default networks.

---

## 6) Default bridge network

Docker creates a default bridge network automatically.

### Example

If you run a container without specifying any network, it usually joins the default bridge network.

```bash
docker run -it ubuntu
```

### Characteristics

* containers get an IP address
* containers can talk to each other using IPs
* name-based DNS is limited compared to a user-defined bridge
* manual linking or IP lookup may be needed in older setups

---

## 7) User-defined bridge network

A **user-defined bridge network** is a bridge network that you create yourself.

### Create a custom bridge network

```bash
docker network create my_bridge
```

### Run containers on it

```bash
docker run -dit --name container_one --network my_bridge alpine sleep 1000
```

```bash
docker run -dit --name container_two --network my_bridge alpine sleep 1000
```

### Why it is better than the default bridge

* automatic DNS resolution by container name
* easier container-to-container communication
* better isolation
* easier to manage in real projects

---

## 8) Default bridge vs user-defined bridge

| Feature                           | Default bridge | User-defined bridge                       |
| --------------------------------- | -------------- | ----------------------------------------- |
| Created automatically             | Yes            | No, you create it                         |
| Name resolution by container name | Limited        | Yes                                       |
| Better isolation                  | No             | Yes                                       |
| Easier to manage                  | Less           | More                                      |
| Best use                          | Quick testing  | Real development and multi-container apps |

### Main difference

The user-defined bridge is usually preferred because containers can communicate by name.

Example:

```bash
ping container_two
```

This works more smoothly on a user-defined bridge network.

---

## 9) What does ping mean?

`ping` is a command used to check whether one machine or container can reach another.

It sends small ICMP packets and waits for a reply.

### What ping tells you

* whether the target is reachable
* whether networking is working
* whether the target IP or name is valid

### Example

```bash
docker exec container_two ping 172.17.0.6
```

### Meaning

* **docker exec**: runs a command inside a running container
* **container_two**: the container where the command is executed
* **ping 172.17.0.6**: checks whether the container can reach the container with that IP address

If the ping succeeds, the two containers can communicate.

---

## 10) What is `docker exec`?

```bash
docker exec container_two ping 172.17.0.6
```

### Meaning

* **docker exec**: executes a command inside a container that is already running
* it does not start a new container
* it is useful for testing, debugging, and checking connectivity

### Example

```bash
docker exec -it container_two sh
```

This opens a shell inside the container.

---

## 11) Example of container communication

Suppose you create a custom bridge network and run two containers.

```bash
docker network create my_bridge
```

```bash
docker run -dit --name container_one --network my_bridge alpine sleep 1000
```

```bash
docker run -dit --name container_two --network my_bridge alpine sleep 1000
```

Now from `container_two`, you can test connectivity:

```bash
docker exec container_two ping container_one
```

Or by IP:

```bash
docker exec container_two ping 172.17.0.6
```

If the containers are on the same bridge network, they can talk to each other.

---

## 12) Host network driver

The **host** network driver makes the container share the host machine’s network directly.

### Meaning

* no separate network namespace for the container
* container uses the host’s IP and ports directly
* no port mapping with `-p` is needed

### Example

```bash
docker run --network host nginx
```

### When it is useful

* high performance networking
* testing network-heavy applications
* when you want direct access to host networking

### Limitation

Less isolation, so it is not always best for production.

---

## 13) Overlay network driver

The **overlay** driver is used to connect containers across multiple Docker hosts.

### Meaning

* used in clustered environments
* often used with Docker Swarm
* enables container communication across machines

### When it is useful

* distributed applications
* microservices running on multiple hosts
* swarm-based deployments

---

## 14) Macvlan network driver

The **macvlan** driver gives each container its own MAC address.

### Meaning

* containers appear like physical devices on the network
* they can get addresses from the same network as your LAN

### When it is useful

* when containers must appear as separate devices
* legacy networking setups

### Limitation

Can be harder to configure and manage.

---

## 15) Ipvlan network driver

The **ipvlan** driver is similar to macvlan, but it uses IP-based networking instead of separate MAC addresses.

### When it is useful

* advanced network control
* fewer MAC address issues than macvlan

---

## 16) None network driver

The **none** driver disables networking for the container.

### Meaning

* container has no network access
* useful for isolated jobs or special security use cases

### Example

```bash
docker run --network none alpine
```

---

## 17) Quick command reference

```bash
# List networks
docker network ls

# Create a custom bridge network
docker network create my_bridge

# Run containers on that network
docker run -dit --name container_one --network my_bridge alpine sleep 1000
docker run -dit --name container_two --network my_bridge alpine sleep 1000

# Check connectivity
docker exec container_two ping container_one

# Ping a container IP
docker exec container_two ping 172.17.0.6

# Run with host network
docker run --network host nginx

# Run without networking
docker run --network none alpine
```

---

## 18) Best practice

For most normal applications, use a **user-defined bridge network**.

Why?

* easy container name resolution
* good isolation
* simple setup
* perfect for app + database + cache style projects

---

## 19) Final summary

* **Bridge network**: private network for containers on the same host
* **Default bridge**: automatic, basic, less convenient
* **User-defined bridge**: custom, better DNS, better for real projects
* **Ping**: checks whether one container can reach another
* **docker exec**: runs commands inside a running container
* **Host**: container shares host networking
* **Overlay**: network across multiple hosts
* **Macvlan / Ipvlan**: advanced network drivers
* **None**: no networking

Docker networking is important because it makes containers communicate safely and correctly in real applications.
