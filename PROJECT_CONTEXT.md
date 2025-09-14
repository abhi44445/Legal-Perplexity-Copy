# Legal Perplexity 2.0 - Project Context & Status

## Project Overview
**Goal**: Transform Legal Perplexity from Streamlit to modern React/FastAPI application with sophisticated legal AI dashboard interface.

**Tech Stack**:
- Backend: FastAPI (Python) - ✅ COMPLETED
- Frontend: React + Vite (JSX), Tailwind CSS v4, shadcn/ui components
- Database: Existing constitution vectorstore with FAISS
- AI: Constitutional RAG system with citation support

## Current Project Status (December 2024)

### ✅ COMPLETED COMPONENTS
1. **Backend API Architecture** - Fully functional FastAPI server
   - Constitution chat endpoints (`/api/constitution/`)
   - Rights exploration (`/api/rights/`)
   - Cases database (`/api/cases/`)
   - Research workspace (`/api/research/`)
   - Server running on http://localhost:8000

2. **Core UI Component Library** - All converted to JSX format
   - ✅ Sidebar component with collapsible navigation
   - ✅ Command palette component with cmdk integration
   - ✅ Sheet component for mobile overlays
   - ✅ Badge component for status indicators
   - ✅ Dialog component for modals
   - ✅ Tooltip component with Radix UI
   - ✅ Button and Card components (Tailwind v4 compatible)

3. **App Shell Infrastructure**
   - ✅ Main App.jsx with routing structure
   - ✅ AppSidebar with navigation menu
   - ✅ AppHeader with search trigger
   - ✅ CommandPalette with keyboard shortcuts (Cmd+K)
   - ✅ React Router DOM integration

4. **Dependencies Installed**
   - ✅ @radix-ui/react-dialog
   - ✅ @radix-ui/react-tooltip  
   - ✅ @radix-ui/react-slot
   - ✅ react-router-dom
   - ✅ cmdk for command palette
   - ✅ Tailwind CSS v4 configured
   - ✅ Framer Motion for animations

### 🚧 IN PROGRESS
- App shell layout (basic structure created, needs page components)

### ❌ PENDING PAGES & FEATURES
1. **Dashboard Homepage** - Modern dashboard replacing basic grid
2. **Constitution Chat Interface** - Advanced chat UI with message bubbles
3. **Rights Explorer Page** - Interactive rights browser with filtering
4. **Cases Database Interface** - Comprehensive case management
5. **Research Workspace** - Document comparison and note-taking
6. **Search Results Page** - Unified search with filtering
7. **Mobile Responsive Design** - Touch-friendly interactions
8. **Dark Mode Implementation** - Theme toggle and persistence
9. **Loading & Error States** - Skeletons and error boundaries
10. **Performance Optimizations** - Code splitting and lazy loading
11. **Accessibility Improvements** - WCAG 2.1 AA compliance
12. **Animation & Transitions** - Framer Motion integration
13. **API Integration Updates** - Connect new UI to existing APIs
14. **Testing Implementation** - Playwright E2E tests
15. **Documentation & Deployment** - README and build config

## File Structure Status

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── ✅ sidebar.jsx (converted from TSX)
│   │   │   ├── ✅ command.jsx (converted from TSX)
│   │   │   ├── ✅ sheet.jsx (converted from TSX)
│   │   │   ├── ✅ badge.jsx (converted from TSX)
│   │   │   ├── ✅ dialog.jsx (converted from TSX)
│   │   │   ├── ✅ tooltip.jsx (converted from TSX)
│   │   │   ├── ✅ button.jsx (Tailwind v4 compatible)
│   │   │   └── ✅ card.jsx (Tailwind v4 compatible)
│   │   ├── ✅ AppSidebar.jsx (navigation menu)
│   │   ├── ✅ AppHeader.jsx (header with search)
│   │   └── ✅ CommandPalette.jsx (Cmd+K shortcuts)
│   ├── pages/
│   │   ├── ✅ HomePage.jsx (basic, needs modern dashboard)
│   │   ├── ❌ ConstitutionChat.jsx (needs creation)
│   │   ├── ❌ RightsExplorer.jsx (needs creation)
│   │   ├── ❌ CasesDatabase.jsx (needs creation)
│   │   ├── ❌ ResearchWorkspace.jsx (needs creation)
│   │   └── ❌ SearchResults.jsx (needs creation)
│   ├── hooks/
│   │   └── ✅ use-mobile.jsx (responsive hook)
│   ├── lib/
│   │   └── ✅ utils.js (cn function for class merging)
│   ├── ✅ App.jsx (shell with routing)
│   └── ✅ main.jsx (entry point)
├── ✅ package.json (all dependencies installed)
├── ✅ tailwind.config.js (v4 configuration)
├── ✅ postcss.config.js (fixed for v4)
└── ✅ vite.config.js
```

## Backend API Endpoints (Ready for Integration)

### Constitution Chat API
```
POST /api/constitution/chat
- Input: {"query": "constitutional question"}
- Output: {"response": "AI answer", "sources": [...]}
```

### Rights API
```
GET /api/rights/
- Returns: List of fundamental rights with metadata
GET /api/rights/search?q=query
- Returns: Filtered rights based on search
```

### Cases API
```
GET /api/cases/
- Returns: Legal cases database
GET /api/cases/search?q=query
- Returns: Filtered cases
```

### Research API
```
GET /api/research/
- Returns: Research documents and notes
POST /api/research/analyze
- Input: {"text": "legal document"}
- Output: Analysis and insights
```

## Design Requirements

### User Interface Priorities
1. **Legal Professional Focus** - Clean, professional interface for lawyers and legal researchers
2. **AI-First Design** - Prominent chat interface with constitutional AI assistant
3. **Document-Centric** - Easy access to constitution text, cases, and legal documents
4. **Search-Driven** - Powerful search with command palette (Cmd+K)
5. **Research Workflow** - Note-taking, bookmarking, citation management

### Component Design Patterns
- **Sidebar Navigation**: Collapsible with Constitution/Rights/Cases/Research sections
- **Command Palette**: Global search and navigation (Cmd+K trigger)
- **Dashboard Cards**: Quick stats, recent activity, action shortcuts
- **Chat Interface**: Message bubbles with source citations
- **Table/Grid Views**: For cases and rights with filtering
- **Modal Overlays**: For detailed views and forms

### Mobile Considerations
- Touch-friendly sidebar that slides over content
- Command palette adapted for mobile search
- Responsive grid layouts for cards and tables
- Mobile-optimized chat interface

## Technical Constraints & Requirements

### JSX Compatibility
- All shadcn/ui components converted from TSX to JSX
- No TypeScript interfaces - use PropTypes if needed
- React functional components with hooks

### Tailwind CSS v4
- Using @tailwind base/components/utilities
- Custom CSS variables for theming
- PostCSS configuration updated for v4

### Performance Requirements
- Code splitting for page components
- Lazy loading for heavy components
- React.memo for expensive renders
- Optimistic updates for API calls

### Accessibility Standards
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Focus management for modals

## Next Steps for Agent

When an agent picks up this project, they should:

1. **Assess Current State**: Review completed components and running backend
2. **Create Todo Plan**: Generate specific, actionable todos for remaining features
3. **Start with HomePage**: Modernize dashboard with stats and action cards
4. **Build Page by Page**: Create ConstitutionChat, RightsExplorer, etc.
5. **Test Integration**: Ensure all components work with existing APIs
6. **Add Polish**: Animations, loading states, error handling
7. **Mobile Optimization**: Responsive design and touch interactions
8. **Performance Tuning**: Code splitting and optimization
9. **Testing Suite**: Playwright E2E tests for critical flows
10. **Production Prep**: Build optimization and deployment config

## Current Development Environment

```bash
# Frontend (working directory)
cd E:\MyProjects\LegalPerplexity2.0\frontend
npm run dev  # Vite dev server on http://localhost:5173

# Backend (separate terminal)
cd E:\MyProjects\LegalPerplexity2.0
python run_constitution_chat.py  # FastAPI on http://localhost:8000
```

## Key Design References
- User previously referenced: https://github.com/abhi44445/cogni-law.git (TSX format)
- Following modern legal AI dashboard patterns
- Anthropic Claude-style interface elements
- Professional legal software UX patterns

---

**Last Updated**: December 2024
**Status**: Ready for UI page development and API integration
**Priority**: Complete modern dashboard homepage and chat interface