# POC – NestJS + PostgreSQL

## Introduction
This Proof of Concept was created to test the NestJS stack with PostgreSQL.  
The goal was to evaluate the strengths and limitations of this combination, particularly in terms of security, documentation, and practicality for a medium-sized project.

---

## NestJS (including Swagger)

Advantages:  
- Clear and modular architecture (modules, services, decorators).  
- Built-in security: guards (`JwtAuthGuard`, `RolesGuard`), useful decorators (`@Roles()`, `@UserId()`), fine-grained permission management.  
- Automatic API documentation with Swagger using decorators (`@ApiOperation`, `@ApiResponse`, etc.). Very practical for testing and sharing the API.  
- High flexibility and scalability: suitable for medium to large projects.  
- Large community and rich ecosystem around TypeScript and Node.js.  

Disadvantages:  
- Steeper learning curve, especially for guards, JWT strategy, and dependency injection.  
- Can feel heavy for a small project (a lot of boilerplate).  
- Swagger, while automatic, requires extra effort on DTOs for complete documentation.  

---

## PostgreSQL

Advantages:  
- Robust and performant database, widely proven in production.  
- Supports advanced features: transactions, indexes, JSONB, stored procedures.  
- Very good integration with TypeORM and NestJS.  
- Reliable and stable.  

Disadvantages:  
- Might be overkill if only simple features are used.  
- More complex than lighter solutions (e.g., SQLite).  
- Initial setup heavier for a simple POC.  

---

## Conclusion
- NestJS is a complete and secure framework, well-suited for structured and scalable projects, but probably too ambitious for a small project.  
- PostgreSQL is a reliable and powerful database, though many advanced features are not fully used in this POC.  
- The integration of Swagger in NestJS is a real plus for documenting and quickly testing endpoints.  

---

## Personal Opinion
JavaScript/TypeScript offer a huge range of possibilities and libraries. It’s very powerful, but sometimes almost too detailed for a simple project.  
In this POC, I found that NestJS and PostgreSQL bring a lot of security, structure, and performance. However, I don’t use all the features, which makes the stack feel a bit “overkill” for the current needs.  
I especially appreciate the security provided by NestJS (guards, roles, decorators) and the convenience of Swagger for documentation—these are two points that I find really essential.  

---

## Getting Started (Docker)

### Prerequisites
- Docker and Docker Compose installed

### Running the Project
From the root folder (where the `docker-compose.yml` is located):

```bash
# Start the containers
docker-compose up --build

.
├── api
│   ├── Dockerfile
│   ├── eslint.config.mjs
│   ├── nest-cli.json
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   ├── src
│   │   ├── app.controller.ts
│   │   ├── app.module.ts
│   │   ├── app.service.ts
│   │   ├── auth
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.module.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── dto
│   │   │   │   ├── login.dto.ts
│   │   │   │   └── register.dto.ts
│   │   │   └── jwt.strategy.ts
│   │   ├── common
│   │   │   ├── decorators
│   │   │   │   ├── public.decorator.ts
│   │   │   │   ├── roles.decorator.ts
│   │   │   │   └── user.decorator.ts
│   │   │   ├── dto
│   │   │   ├── enum
│   │   │   │   └── role.enum.ts
│   │   │   └── guards
│   │   │       ├── jwtAuth.guard.ts
│   │   │       └── roles.guard.ts
│   │   ├── config
│   │   │   └── database.config.ts
│   │   ├── env.validation.ts
│   │   ├── main.ts
│   │   └── users
│   │       ├── dto
│   │       │   ├── create_user.dto.ts
│   │       │   ├── update_user.dto.ts
│   │       │   └── user.dto.ts
│   │       ├── user.entity.ts
│   │       ├── users.controller.ts
│   │       ├── users.module.ts
│   │       └── users.service.ts
│   ├── test
│   │   ├── app.e2e-spec.ts
│   │   └── jest-e2e.json
│   ├── tsconfig.build.json
│   └── tsconfig.json
├── db
└── docker-compose.yml
