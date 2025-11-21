# DevOps Technical Documentation

## Infrastructure
-   **Cloud**: AWS EC2 (t2.micro or similar)
-   **OS**: Ubuntu / Amazon Linux 2
-   **Container Runtime**: Docker Engine + Docker Compose

## CI/CD Pipeline
-   **Tool**: Jenkins
-   **Type**: Declarative Pipeline
-   **SCM**: Git (Polling every 2 mins)

## Deployment Strategy
-   **Rolling Update**: We use `docker-compose up -d` which replaces containers.
-   **Network**: All containers share a bridge network `fullstack_container_default`.

## Ports
-   **Public**: 8000 (API), 3000 (Frontend)
-   **Private**: 3306 (MySQL - accessible only within Docker network)
