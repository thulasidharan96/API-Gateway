# Deployment

- Build image: `docker build -t api-gateway:latest .`
- Run stack: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
- Use managed Postgres/Redis in production and rotate JWT secrets regularly.
