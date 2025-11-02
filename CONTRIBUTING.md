# Contributing to AREA

Welcome to the AREA project. This guide will help you get started with contributing to the application.

## Overview

AREA is an automation platform that connects various services through action-reaction workflows. The project consists of:

- **Frontend**: Next.js web application
- **Server**: FastAPI backend server
- **Mobile**: Flutter mobile application

## Documentation Structure

This is the quick-start guide. For detailed component-specific information:

- [Frontend Contributing Guide](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide) - Technology stack, project structure, code standards
- [Server Contributing Guide](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide) - API development, service integration, database management
- [Service Implementation Guides](https://github.com/Area-dreamteam/Area/wiki) - OAuth services, Actions/Reactions

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.10+ (for local server development)

### Setup and Run

1. Clone the repository and navigate to it

2. Set up environment files in `frontend/.env` and `server/.env`

> [!IMPORTANT]
> Reference `.env.prod` or `.env.tests` for required variables. Never commit these files.

3. Start development environment:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Services will be available at:
- Frontend: `http://localhost:8081`
- Backend API: `http://localhost:8080` (docs at `/docs`)
- PostgreSQL: `localhost:5432`

4. Stop services:

```bash
docker compose -f docker-compose.dev.yml down
# Add -v flag to also remove database volumes
```

## Development Workflow

### 1. Choose Your Component

Select the guide(s) you need:

- **Frontend**: [Getting Started](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#getting-started), [Component Development](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#component-development)
- **Server**: [Getting Started](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#getting-started), [API Development](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#api-development)
- **Service Integration**: [OAuth Service Guide](https://github.com/Area-dreamteam/Area/wiki/Implementation-Guide), [Automation Service Guide](https://github.com/Area-dreamteam/Area/wiki/Service-Implementation-Guide)

### 2. Create Feature Branch

```bash
git checkout -b <type>/description
```

Types: `feature`, `fix`, `docs`, `refactor`, `test`, `chore`

### 3. Code Standards

**Frontend**:
- See [Code Standards](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#code-standards)
- TypeScript strict mode, ESLint, Prettier (single quotes, no semicolons)

**Server**:
- See [Code Standards](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#code-standards)
- PEP 8, type hints, async/await

### 4. Test Your Changes

**Frontend**:
```bash
cd frontend
npm run test
npm run lint
```

**Server**:
```bash
cd server
pytest
```

> [!WARNING]
> All tests must pass before submitting a PR. CI/CD will automatically run tests.

### 5. Commit and Push

Use conventional commit format:

```bash
git commit -m "feat(scope): description"    # New feature
git commit -m "fix(scope): description"     # Bug fix
git commit -m "docs(scope): description"    # Documentation
```

### 6. Create Pull Request

Include:
- Clear title and description
- Reference related issues
- Screenshots for UI changes

## Common Tasks

### Adding a New Page

See: [Frontend - Adding a New Page](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#adding-a-new-page)

### Adding a New API Endpoint

See: [Server - Creating New Endpoints](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#creating-new-endpoints)

### Adding a New Service Integration

See: [Service Implementation Guide](https://github.com/Area-dreamteam/Area/wiki/Service-Implementation-Guide)

For OAuth login only: [OAuth Service Guide](https://github.com/Area-dreamteam/Area/wiki/Implementation-Guide)

### Working with the Database

See: [Server - Database Management](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#database-management)

Quick access:
```bash
docker exec -it pgdata psql -U <POSTGRES_USER> -d <POSTGRES_DB>
```

## Troubleshooting

### Docker Issues

**Containers won't start**:
```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up --build
```

### Frontend Issues

See: [Frontend - Troubleshooting](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#troubleshooting)

**Quick fix for module errors**:
```bash
cd frontend && rm -rf node_modules .next && npm install
```

### Server Issues

See: [Server - Troubleshooting](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#troubleshooting)

**Quick fix for import errors**:
```bash
cd server && source .venv/bin/activate && pip install -r requirements.txt
```

## Project Structure

```
Area/
├── frontend/         # Next.js web app (port 8081)
│   ├── app/          # Routes and page components
│   └── components/   # Reusable UI components
├── server/           # FastAPI backend (port 8080)
│   └── app/
│       ├── api/      # API endpoints
│       ├── models/   # Database models
│       └── services/ # External service integrations
└── mobile/           # Flutter mobile app
```

Full structure details:
- [Frontend Structure](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#project-structure)
- [Server Structure](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#project-structure)

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Code Review Guidelines

Reviewers should check:
1. Functionality and tests
2. Code quality and standards
3. Documentation completeness
4. Performance and security implications

## Best Practices

### General
- Keep functions small and focused
- Handle errors gracefully
- Log important events

### Component-Specific
- Frontend: See [Best Practices](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#best-practices)
- Server: See [Best Practices](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#best-practices)

## Security

> [!WARNING]
> Never commit secrets or credentials. Use environment variables for sensitive data.

See:
- [Frontend - Code Standards](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#code-standards)
- [Server - Configuration](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#configuration)

## Testing Strategy

- **Unit tests**: Individual functions/components
- **Integration tests**: API endpoints and database
- **E2E tests**: Complete user workflows

See detailed testing guides:
- [Frontend Testing](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide#testing)
- [Server Testing](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide#testing)

## Continuous Integration

GitHub Actions workflows:
- Backend: pytest, code quality checks
- Frontend: Jest, ESLint, build verification
- Deploy: Automated deployment on success

All checks must pass before merging.

## Resources

### Documentation
- [GitHub Wiki](https://github.com/Area-dreamteam/Area/wiki) - Complete documentation
- [Frontend Guide](https://github.com/Area-dreamteam/Area/wiki/Frontend-Contributing-Guide)
- [Server Guide](https://github.com/Area-dreamteam/Area/wiki/Server-Contributing-Guide)

### Framework Docs
- [Next.js](https://nextjs.org/docs)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## Getting Help

1. Check [GitHub Wiki](https://github.com/Area-dreamteam/Area/wiki)
2. Search existing GitHub issues
3. Review existing code for patterns
4. Create a new issue with details
5. Contact the development team

Thank you for contributing to AREA!
