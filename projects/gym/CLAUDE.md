# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (Vue 3 + Vite + Element Plus)
```bash
cd source/GymReservationSystem/frontend
npm install                    # Install dependencies
npm run dev                    # Start development server (localhost:5173)
npm run build                  # Build for production
npm run preview                # Preview production build
npm run lint                   # Lint with ESLint and auto-fix
npm run format                 # Format code with Prettier
```

### Backend (Spring Boot + Maven)
```bash
cd source/GymReservationSystem/backend
mvn clean install             # Clean and build project
mvn spring-boot:run           # Start development server (localhost:8080)
mvn test                      # Run all tests
mvn package                   # Package as JAR
```

### Database Setup
```bash
# Initialize database and tables
mysql -u root -p < database/complete_init_database.sql

# Insert test data
mysql -u root -p < backend/sql/test-data.sql
```

## Architecture Overview

This is a **Gym Reservation Management System** (健身房预约管理系统) with a full-stack architecture:

### Backend Architecture
- **Spring Boot 2.7.x** with Java 17
- **MyBatis-Plus** for ORM with MySQL 8.x
- **Redis 7.x** for caching and session management
- **Redisson** for distributed locking (reservation conflicts)
- **JWT** for authentication and authorization
- **ZXing** for QR code generation (reservations/check-ins)
- **Apache POI** for Excel report exports
- **Hutool** for utility functions

### Frontend Architecture
- **Vue 3** with Composition API
- **Element Plus** for UI components
- **Pinia** for state management
- **Vue Router** for routing
- **ECharts** for data visualization
- **Axios** for HTTP requests

### Key Domain Concepts
- **Multi-role system**: Regular users, coaches, administrators
- **Reservation system**: Gym venues with time slot booking
- **Course management**: Group classes with instructor scheduling
- **Membership cards**: Various types (session/monthly/yearly) with expiration tracking
- **Check-in system**: QR code scanning for attendance
- **Analytics**: Usage statistics, popular courses, member activity reports

## Code Structure Patterns

### Backend Structure
```
backend/src/main/java/com/gym/reservation/
├── controller/     # REST API endpoints
├── service/        # Business logic
├── entity/         # Database entities
├── mapper/         # MyBatis data access
├── dto/           # Data transfer objects
├── config/        # Configuration classes
├── utils/         # Utility classes
└── exception/     # Custom exceptions
```

### Frontend Structure
```
frontend/src/
├── views/         # Page components
├── components/    # Reusable UI components
├── api/          # HTTP request functions
├── store/        # Pinia state management
├── router/       # Vue Router configuration
├── utils/        # Utility functions
└── styles/       # Global styles
```

## Development Guidelines

### Authentication & Authorization
- All API endpoints require proper role-based access control
- Use JWT tokens for session management
- Implement proper logout and token refresh mechanisms

### Database & Caching
- Use distributed locks (Redisson) for reservation operations to prevent conflicts
- Cache frequently accessed data (venue status, user info, course data) in Redis
- Implement proper cache invalidation strategies

### QR Code Integration
- Generate QR codes using ZXing library for reservations and check-ins
- QR codes should contain URLs with parameters for mobile-friendly scanning

### Testing Strategy
- Write unit tests for all service layer methods
- Test reservation conflict scenarios thoroughly
- Validate role-based access control in controller tests

### Performance Considerations
- Implement pagination for large data sets (member lists, reservation history)
- Use database indexes for frequently queried fields (dates, user IDs, venue IDs)
- Optimize chart data queries for analytics dashboard

## Test Accounts
- **admin/123456** - Administrator (full access)
- **coach1/123456** - Coach (course management, attendance viewing)
- **user1/123456** - Regular user (reservations, course enrollment)