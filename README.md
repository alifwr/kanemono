# Money Tracker - Reference Documents

This directory contains technical reference documentation for the Money Tracker application, split into backend and frontend components.

## 📁 Document Structure

### 1. BACKEND_REFERENCE.md
**For:** Backend developers working with FastAPI, PostgreSQL, and SQLAlchemy

**Contents:**
- ✅ Complete database schema with SQLAlchemy models
- ✅ Backend project structure (FastAPI)
- ✅ Repository and service patterns
- ✅ API endpoint implementations
- ✅ Authentication and security
- ✅ Business logic (balance calculation, budget tracking)
- ✅ Testing strategies
- ✅ Deployment configurations

**Use this when:**
- Setting up the database
- Implementing API endpoints
- Writing business logic
- Configuring authentication
- Writing backend tests

---

### 2. FRONTEND_REFERENCE.md
**For:** Frontend developers working with Nuxt.js, Vue 3, and TypeScript

**Contents:**
- ✅ Complete TypeScript type definitions
- ✅ Frontend project structure (Nuxt.js 3)
- ✅ Composables for API integration
- ✅ Pinia store implementations
- ✅ Component examples (forms, lists, etc.)
- ✅ Utility functions (currency, date formatting)
- ✅ UI/UX patterns
- ✅ Frontend testing

**Use this when:**
- Setting up the frontend project
- Creating components
- Implementing API calls
- Managing state with Pinia
- Writing frontend tests

---

### 3. MONEY_TRACKER_REFERENCE.md (Original)
**For:** Full overview of the entire application

**Contents:**
- ✅ Complete system architecture
- ✅ Both backend and frontend together
- ✅ Integration points between systems
- ✅ Development roadmap
- ✅ BCA-specific requirements

**Use this when:**
- Understanding the full system
- Planning features
- Coordinating between frontend and backend
- Making architectural decisions

---

## 🚀 Quick Start Guide

### For Backend Developers

1. **Read:** `BACKEND_REFERENCE.md`
2. **Focus on:**
   - Database Schema section
   - Backend Architecture section
   - API Endpoints section
3. **Start with:**
   - Set up PostgreSQL
   - Create database migrations
   - Implement authentication
   - Build core API endpoints

### For Frontend Developers

1. **Read:** `FRONTEND_REFERENCE.md`
2. **Focus on:**
   - Type Definitions section
   - API Integration section
   - State Management section
3. **Start with:**
   - Set up Nuxt.js project
   - Configure API base URL
   - Implement authentication flow
   - Build core components

### For Full-Stack Developers

1. **Read:** All three documents
2. **Start with:** `MONEY_TRACKER_REFERENCE.md` for overview
3. **Then refer to:** Specific backend/frontend docs as needed

---

## 📋 Technology Stack Summary

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0 (async)
- **Authentication:** JWT with python-jose
- **Migration:** Alembic

### Frontend
- **Framework:** Nuxt.js 3 (Vue 3)
- **Language:** TypeScript
- **State:** Pinia
- **HTTP:** $fetch / ofetch
- **Date:** Day.js
- **Charts:** Chart.js / ApexCharts

---

## 🔗 Key Integration Points

### Authentication Flow
1. **Frontend** sends credentials → `/api/v1/auth/login`
2. **Backend** validates and returns JWT tokens
3. **Frontend** stores tokens and includes in subsequent requests
4. **Backend** validates token on protected endpoints

### Data Flow Example (Creating Transaction)
1. **Frontend** user fills transaction form
2. **Frontend** validates and sends to `POST /api/v1/transactions`
3. **Backend** validates ownership, creates transaction
4. **Backend** calculates balance, updates account
5. **Backend** returns created transaction
6. **Frontend** updates UI and local state

---

## 📝 Document Usage Tips

### Finding Information Quickly

**Need database structure?**
→ `BACKEND_REFERENCE.md` → Database Schema section

**Need API endpoint details?**
→ `BACKEND_REFERENCE.md` → API Endpoints section

**Need TypeScript types?**
→ `FRONTEND_REFERENCE.md` → Type Definitions section

**Need component examples?**
→ `FRONTEND_REFERENCE.md` → Components section

**Need to understand balance calculation?**
→ `BACKEND_REFERENCE.md` → Business Logic section

**Need IDR formatting?**
→ `FRONTEND_REFERENCE.md` → Utilities section

---

## 🎯 Development Priorities

### Phase 1: Foundation (MVP)
- [ ] Backend: Database setup + Auth
- [ ] Frontend: Project setup + Auth UI
- [ ] Integration: Login/Register flow

### Phase 2: Core Features
- [ ] Backend: Accounts + Transactions API
- [ ] Frontend: Account management + Transaction CRUD
- [ ] Integration: Full transaction workflow

### Phase 3: Advanced Features
- [ ] Backend: Analytics + Budgets
- [ ] Frontend: Dashboard + Charts
- [ ] Integration: Real-time updates

---

## 📞 Common Questions

**Q: Which document should I start with?**
**A:** If you're working on backend only → `BACKEND_REFERENCE.md`
     If you're working on frontend only → `FRONTEND_REFERENCE.md`
     If you need full context → `MONEY_TRACKER_REFERENCE.md`

**Q: Are the API endpoints the same in both documents?**
**A:** Backend doc has implementation details, frontend doc has usage examples. Both describe the same API.

**Q: Can I develop backend and frontend simultaneously?**
**A:** Yes! The API contract in both documents ensures compatibility. Use mock data initially if needed.

**Q: Where are the BCA-specific requirements?**
**A:** Detailed in all three documents, but focus on:
     - Backend: Database schema (transaction fields)
     - Frontend: Currency formatting utilities
     - Full: BCA-Specific Requirements section

---

## 🔄 Keeping Documents in Sync

When making changes:

1. **API changes** → Update both backend and frontend docs
2. **Database changes** → Update backend doc + full reference
3. **UI changes** → Update frontend doc
4. **New features** → Update all three documents

---

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Nuxt.js Documentation: https://nuxt.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Vue 3 Documentation: https://vuejs.org/guide/
- Pinia Documentation: https://pinia.vuejs.org/

---

**Last Updated:** 2025-10-25  
**Version:** 1.0
