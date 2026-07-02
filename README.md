# ClickLive 
### High-Performance, Real-Time Clickstream Ingestion Pipeline

ClickLive is a production-grade, event-driven backend architecture designed to handle high-velocity user activity data (clicks, views, transactions) without overwhelming persistent storage. By decoupling the API ingestion layer from the database worker layer using a message queue, the system can withstand massive traffic spikes seamlessly.

---

##  System Architecture

The architecture is entirely containerized and split into four specialized, independent services:

1. **Ingestion Gateway (`main.py`):** An asynchronous FastAPI web server that acts as the entry portal. It accepts incoming user tracking data instantly (sub-millisecond response time) and throws it directly into the queue.
2. **Buffer Queue (Redis):** An in-memory, high-speed data structure store acting as a message broker. It stores incoming traffic sequentially so no data drops during traffic surges.
3. **Stream Consumer (`worker.py`):** A detached background worker node that continuously polls the Redis queue, processes payloads, and handles bulk insertion into the archive.
4. **Data Archive (PostgreSQL):** The permanent relational database storage layer where event data is securely structured and archived.
5. **Telemetry Dashboard (`index.html`):** A real-time monitoring view powered by **WebSockets** that pushes live backend data streams directly to the UI with zero browser-refresh latency.

---

##  Tech Stack & Concepts Demonstrated

* **Language:** Python 3.10+
* **Framework:** FastAPI (Asynchronous Server)
* **Message Broker:** Redis (FIFO Queue & Pub/Sub)
* **Database:** PostgreSQL (SQL Storage)
* **Containerization:** Docker & Docker Compose
* **Protocols:** HTTP (REST API) & WebSockets (Live Telemetry Streaming)
* **Architecture Pattern:** Decoupled Event-Driven Microservices

---

##  Quick Start / Local Deployment

This entire pipeline is configured to spin up with a single command using Docker.

### Prerequisites
* Docker and Docker Compose installed on your machine.

### Spin up the Architecture
Clone this repository, navigate to the folder, and run:
```bash
docker-compose up --build
