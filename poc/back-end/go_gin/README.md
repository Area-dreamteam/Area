# POC – Go (Gin) + Neo4j

## Introduction
This Proof of Concept was created to test the **Gin framework in Go** with **Neo4j**.
The goal was to evaluate the strengths and limitations of this stack, focusing on performance, graph-based data modeling, and practicality for a small to medium-sized project.

---

## Gin Framework

**Advantages:**
- Lightweight and fast HTTP framework, close to net/http but with better ergonomics.
- Simple routing with middleware support.
- Clear separation possible between models, routes, services, and utilities.
- Easy to get started and build REST APIs quickly.
- Strong performance due to Go’s concurrency model (goroutines, channels).

**Disadvantages:**
- Minimalistic: lacks built-in features (authentication, validation, documentation) compared to larger frameworks like NestJS or Spring.
- Swagger/OpenAPI integration requires external libraries (e.g., `swaggo`).
- Dependency injection is manual (no built-in DI container).
- Can lead to less structured code if not organized properly.

---

## Neo4j

**Advantages:**
- Designed for graph-based relationships, ideal for use cases like social networks, recommendations, fraud detection, and knowledge graphs.
- Query language (Cypher) is expressive and easy to learn.
- Handles complex relationships much more naturally than relational databases.
- Strong ecosystem with official Go driver (`neo4j-go-driver`).

**Disadvantages:**
- Not as widely adopted as relational databases (e.g., PostgreSQL), meaning smaller ecosystem and fewer tutorials.
- Requires a different mindset than relational data modeling.
- For simple CRUD use cases, Neo4j may be overkill compared to traditional SQL databases.
- Running Neo4j in Docker can be heavier than lighter databases.

---

## Conclusion
- **Gin** is excellent for building lightweight and fast APIs. It gives flexibility but requires discipline to keep the code structured.
- **Neo4j** is a great fit for relationship-heavy data models, but may feel unnecessary for simple CRUD projects.
- Together, this stack is well-suited for graph-centric domains, though it requires more setup and knowledge compared to classic Go + SQL projects.

---

## Personal Opinion
Go with Gin feels **fast and minimal**, which I enjoy for prototyping APIs.
Using Neo4j requires a shift in the way of making queries but the cypher language is quite powerful.
It we do need to take into consideration that this database is on the heavy side and thus maybe not appropriated for our uses cases.

---

## Getting Started (Docker)

### Prerequisites
- Docker and Docker Compose installed

### Running the Project
From the root folder (where the `docker-compose.yml` is located):

```bash
docker-compose up --build
```

