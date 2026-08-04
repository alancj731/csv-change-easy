# CSV Processor

A web app that lets you transform CSV files using natural language. Powered by DeepSeek AI.

Upload a CSV, describe what you want in plain English (e.g. "remove rows where age < 18"), review the generated pandas code, edit if needed, and download the result.

## Features

- **Natural language CSV transformation** — describe changes in plain English, AI generates pandas code
- **Code review** — inspect and edit generated code before running
- **Version history** — every change creates a version, revert to any previous state
- **Analysis queries** — ask questions about your data without modifying it
- **Authentication** — Firebase auth (Google + email/password)
- **Rate limiting** — anonymous: 1MB upload / 3 queries per day; authenticated: 4MB / 10 per day

## Tech Stack

- **Frontend**: Vue 3 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI**: DeepSeek API (generates pandas code from natural language)
- **Auth**: Firebase Authentication
- **Rate limiting**: SQLite

## Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- DeepSeek API key
- Firebase project (for authentication)

## Setup

### 1. Clone and install

```bash
git clone <repo-url>
cd process-csv
make install
```

Or manually:

```bash
# Backend
cd backend
uv venv .venv
uv pip install -e ".[dev]"
cd ..

# Frontend
cd frontend
npm install
```

### 2. Configure environment variables

**Backend** — create `backend/.env`:

```env
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
FIREBASE_PROJECT_ID=your-firebase-project-id
```

Get your DeepSeek API key from the DeepSeek platform.

**Frontend** — create `frontend/.env`:

```env
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
```

Get these from your [Firebase Console](https://console.firebase.google.com/) > Project Settings.

### 3. Firebase setup

1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com/)
2. Enable **Authentication** > Sign-in method > Google and Email/Password
3. Add `localhost` to authorized domains (Authentication > Settings)

No service account JSON is needed — the backend verifies tokens using Google's public certificates.

### 4. Run

In two terminals:

```bash
# Terminal 1 — Backend (port 8000)
make dev-backend

# Terminal 2 — Frontend (port 5173)
make dev-frontend
```

Open http://localhost:5173

## Usage

1. **Upload** a CSV file (drag & drop or click to browse)
2. **Describe** what you want to do in plain English
3. **Review** the generated pandas code — edit if needed
4. **Run** the code to apply the transformation
5. **Repeat** — each change creates a version you can revert to
6. **Download** the result CSV when done

### Example queries

**Transform queries** (modify the data):
- "Remove rows where age is less than 18"
- "Add a column called full_name that combines first_name and last_name"
- "Sort by salary descending"
- "Remove duplicate rows based on email"

**Analysis queries** (inspect without changing):
- "How many rows have the same name as other rows?"
- "What is the average salary by department?"
- "Show the top 5 most common values in the city column"

## Rate Limits

| | File size | Conversions/day |
|---|---|---|
| Anonymous | 1 MB | 3 |
| Signed in | 50 MB | 10 |

Need more? Contact winnipegdatafan@gmail.com.

Localhost (`127.0.0.1`) bypasses rate limits for development.

## Project Structure

```
process-csv/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, lifespan
│   │   ├── config.py            # Settings (env vars)
│   │   ├── dependencies.py      # Auth dependency
│   │   ├── exceptions.py        # Error handlers
│   │   ├── routers/
│   │   │   ├── upload.py        # POST /api/upload
│   │   │   ├── query.py         # POST /api/sessions/{id}/generate & /execute
│   │   │   ├── versions.py      # GET versions, POST revert
│   │   │   └── download.py      # GET /api/sessions/{id}/download
│   │   └── services/
│   │       ├── ai_service.py    # DeepSeek code generation + sandboxed execution
│   │       ├── auth_service.py  # Firebase token verification (no service account needed)
│   │       ├── csv_service.py   # CSV read/write/preview
│   │       ├── rate_limiter.py  # SQLite-based rate limiting
│   │       ├── session_manager.py
│   │       └── version_service.py
│   └── data/                    # SQLite DB (auto-created, gitignored)
├── frontend/
│   └── src/
│       ├── api/client.ts        # Axios client with auth interceptor
│       ├── composables/         # useAuth, useSession, useCsvPreview, useVersions, useQueryHistory
│       ├── components/          # FileUpload, CsvTable, QueryInput, CodeEditor, AuthButton, etc.
│       └── views/               # UploadView, WorkspaceView
└── Makefile
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload` | Upload CSV, create session |
| GET | `/api/sessions/{id}/preview` | Paginated data preview |
| POST | `/api/sessions/{id}/generate` | Generate pandas code from natural language |
| POST | `/api/sessions/{id}/execute` | Execute code against current data |
| GET | `/api/sessions/{id}/versions` | List all versions |
| POST | `/api/sessions/{id}/versions/{vid}/revert` | Revert to a version |
| GET | `/api/sessions/{id}/download` | Download current CSV |
