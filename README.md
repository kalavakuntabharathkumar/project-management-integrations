# Project Management Suite with Third-Party Integrations

Next.js frontend + FastAPI backend + MongoDB + RabbitMQ with webhook processing, document upload to S3, and CI.

## Features
- Projects, tasks, assignments, priorities, statuses and dependencies
- Slack, Google Calendar and Stripe webhook adapters
- Retry and idempotency handling
- RabbitMQ event queue
- Document upload endpoint using AWS S3
- Pytest API tests and Cypress smoke test
- GitHub Actions CI

## Run
`docker compose up --build`

Web: http://localhost:3000
API: http://localhost:8000/docs

Copy `.env.example` to `.env` for cloud integrations.
