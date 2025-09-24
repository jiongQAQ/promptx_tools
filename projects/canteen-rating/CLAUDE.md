# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **canteen-rating** project template system designed for graduation thesis development. It supports dual architecture modes and provides a complete full-stack solution with automated development workflows.

## Architecture Modes

### Mode A: Small Program Mode
- **Stack**: Spring Boot + UniApp + Vue Admin
- **Target**: Mobile-first applications, WeChat ecosystem
- **Platforms**: WeChat Mini Program, Alipay, H5

### Mode B: Pure Web Mode
- **Stack**: Spring Boot + Vue User Frontend + Vue Admin
- **Target**: Desktop/laptop users, complex interactions
- **Benefits**: Better SEO and web accessibility

## Project Structure

```
source/canteen-rating-template-2/project/
├── backend/          # Spring Boot 2.7.18, Java 17, MySQL
├── admin_front/      # Vue 3 + Element Plus admin interface (shared)
├── user_front/       # Vue 3 + Element Plus user interface (Mode B only)
└── mini_program/     # UniApp mini program (Mode A only)
```

## Commands for Development

### Backend (Spring Boot)
```bash
cd source/canteen-rating-template-2/project/backend
mvn clean install          # Install dependencies
mvn spring-boot:run        # Start development server (port 8080)
mvn test                   # Run tests
mvn package               # Build JAR file
```

### Admin Frontend (Vue 3)
```bash
cd source/canteen-rating-template-2/project/admin_front
npm install               # Install dependencies
npm run dev              # Start development server (port 5173)
npm run build            # Build for production
npm run lint             # ESLint with auto-fix
```

### User Frontend (Vue 3 - Mode B)
```bash
cd source/canteen-rating-template-2/project/user_front
npm install               # Install dependencies
npm run dev              # Start development server (port 5174)
npm run build            # Build for production
npm run lint             # ESLint with auto-fix
npm run format           # Prettier formatting
```

### Mini Program (UniApp - Mode A)
```bash
cd source/canteen-rating-template-2/project/mini_program
npm install               # Install dependencies
npm run dev:mp-weixin    # WeChat Mini Program development
npm run dev:mp-alipay    # Alipay Mini Program development
npm run dev:h5           # H5 version development
npm run build:mp-weixin  # Build WeChat Mini Program
```

### Project Management Scripts
```bash
# In project/ directory
./start-all.sh           # Start all services (backend + frontends)
./stop-all.sh            # Stop all services
./status.sh              # Check service status
```

### Workflow Automation
```bash
# Execute thesis development workflows
./run-workflow.sh 01                    # Outline generation
./run-workflow.sh 01-1                  # Entity identification
./run-workflow.sh 01-2                  # ER diagram generation
./run-workflow.sh 02                    # Content planning
./run-workflow.sh 02-1                  # Chapter splitting
./run-workflow.sh 03 1                  # Chapter 1 content generation
```

## Key Architecture Principles

### Backend Architecture
- **Package Structure**: Standard Spring Boot layered architecture
  - `controller/` - REST endpoints by user type (auth, user, admin, common)
  - `service/` - Business logic layer
  - `mapper/` - MyBatis Plus data access layer
  - `entity/` - Database entities with logical delete support
- **API Patterns**: `/api/{auth|user|admin|common}/*`
- **Security**: JWT-based authentication with Spring Security
- **Database**: MySQL with MyBatis Plus ORM, H2 for testing

### Frontend Architecture
- **Framework**: Vue 3 Composition API with `<script setup>`
- **State Management**: Pinia stores for global state
- **UI Framework**: Element Plus with auto-import via unplugin
- **Build System**: Vite with SCSS preprocessing
- **Authentication**: JWT tokens with Axios interceptors

### UniApp Architecture (Mode A)
- **Framework**: UniApp 3.x with Vue 3 Composition API
- **UI Library**: uView UI for multi-platform consistency
- **Build System**: Vite-based for faster development

## Development Ports

| Service | Port | Access URL | Description |
|---------|------|------------|-------------|
| Backend | 8080 | http://localhost:8080 | Spring Boot API |
| Admin Frontend | 5173 | http://localhost:5173 | Management interface |
| User Frontend | 5174 | http://localhost:5174 | User interface |

## API Documentation

- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **API Docs**: http://localhost:8080/v3/api-docs

## Technology Specifications

### Backend Stack
- **Framework**: Spring Boot 2.7.18
- **Java Version**: 17
- **Database**: MySQL 8.0+, MyBatis Plus 3.5.3.1
- **Security**: Spring Security + JWT (jsonwebtoken 0.11.5)
- **Documentation**: SpringDoc OpenAPI 1.7.0
- **Build Tool**: Maven

### Frontend Stack
- **Framework**: Vue 3.3.4
- **Router**: Vue Router 4.2.4
- **State**: Pinia 2.1.6
- **UI**: Element Plus 2.3.8
- **HTTP**: Axios 1.4.0
- **Build**: Vite 4.4.5
- **Styling**: SCSS (sass 1.64.1)
- **Linting**: ESLint 8.45.0

## BMAD Workflow Integration

This project uses specialized development agents and workflow automation:
- Database validation (max 15 tables)
- API contract enforcement
- Frontend scope control
- Automated quality assurance
- Entity-database synchronization checks

## Environment Requirements

- **Java**: JDK 17+
- **Node.js**: 16+
- **Maven**: 3.6+
- **MySQL**: 8.0+

## Default Credentials

- **Admin Username**: admin
- **Admin Password**: admin123