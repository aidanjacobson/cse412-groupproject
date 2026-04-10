# Event Manager - Fullstack Database Application

CSE412 Phase 03 project: Full-stack web application with backend API and frontend UI for managing university events, departments, locations, and categories.

**Note:** The database comes pre-populated with data (departments, locations, categories, events) from the shared pgadmin instance. Both development and deployment start with this seed data.

---

## DEVELOPMENT

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker + Docker Compose (Linux)
- Visual Studio Code
- Git

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/aidanjacobson/cse412-groupproject
   cd cse412-groupproject
   ```

2. **Open in VSCode**
   ```bash
   code .
   ```

3. **Open in Dev Container**
   - VSCode will detect the `.devcontainer/devcontainer.json` file
   - Click "Reopen in Container" in the popup, or
   - Press `Ctrl+Shift+P` → search "Dev Container: Reopen in Container"
   - Wait for the container to build and start

4. **Verify Setup**
   - Open terminal in VSCode (should be inside the devcontainer)
   - Connect to database:
     ```bash
     psql -h postgres -U postgres -d eventdb
     ```
   - You should see the `eventdb=#` prompt
   - Database is pre-populated with seed data (departments, locations, categories, events)
   - Type `\q` or `exit` to exit.

5. **Start Development Server**
   ```bash
   python backend/main.py
   ```
   Server runs at `http://localhost:8080`

### Branch Rules

⚠️ **DO NOT push directly to `main`**

1. Create a feature branch:
   ```bash
   git checkout -b [branchname]
   ```

2. Commit and push your changes:
   ```bash
   git push origin [branchname]
   ```

3. Open a **Pull Request** on GitHub
   - Title should reference what you changed
   - You can approve your own PR

4. Merge via GitHub (do not merge locally)

### Project Structure

```
cse412-groupproject/
├── backend/
│   ├── main.py              # Server entry point
│   ├── server.py            # FastAPI app setup
│   ├── requirements.txt      # Python dependencies
│   ├── models/              # Data models (Department, Location, etc.)
│   ├── services/            # DatabaseService (CRUD operations)
│   └── www/                 # Frontend files (HTML, CSS, JS)
├── db_init.sql              # Database schema and seed data
├── docker-compose.yml       # Production compose file
├── docker-compose.dev.yml   # Development compose file
├── Dockerfile               # Production backend image
├── Dockerfile.dev           # Development backend image
├── ROUTES.md                # API endpoint documentation
├── FRONTEND.md              # Frontend development guide
└── README.md                # This file
```
---
## API Documentation

See `ROUTES.md` for all API endpoints.

**Base URL:** `http://localhost:8080/api`

**Main Endpoints:**
- `GET /events` — List all events
- `POST /events` — Create event
- `GET /events/{id}` — Get event details
- `PUT /events/{id}` — Update event
- `DELETE /events/{id}` — Delete event
- `GET /departments`, `/locations`, `/categories` — List reference data

---

## Frontend Development

See `FRONTEND.md` for frontend development responsibilities and requirements.



---

## DEPLOYMENT

### Prerequisites
- Docker
- Docker Compose
- Environment variables file (`.env`)

### Setup

1. **Create `.env` file** in project root:
   ```bash
   POSTGRES_DB=eventdb
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   PORT=8080
   ```

2. **Start Services**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

   This will:
   - Build the backend image
   - Start PostgreSQL container
   - Start backend API container
   - Initialize database with `db_init.sql` (includes all seed data from shared pgadmin instance)

3. **Verify Deployment**
   ```bash
   # Check container status
   docker-compose ps

   # Check logs
   docker-compose logs app
   docker-compose logs postgres
   ```

4. **Access Application**
   - Frontend: `http://localhost:8080`
   - API: `http://localhost:8080/api`
   - Database: `localhost:5432`

### Stopping Services

```bash
# Stop all containers (keep data)
docker-compose down

# Stop and remove all volumes (delete data)
docker-compose down -v
```

---