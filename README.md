# wfAI - AI Chat Application with Persona Management

A modern AI chat application built with clean architecture principles, featuring customizable AI personas, web search capabilities, and memory management through vector storage.

## Features

- **AI Chat Interface**: Real-time streaming responses with markdown support
- **Custom Personas**: Create and manage AI personas with custom icons and personalities
- **Web Search Integration**: Enhance AI responses with real-time web search via SearXNG
- **Memory System**: Vector-based memory storage for contextual conversations
- **Session Management**: Persistent chat sessions with full history
- **Theme Support**: Dark and light mode toggle
- **Clean Architecture**: Domain-driven design with dependency injection

## Architecture

The project follows **Clean Architecture** principles with clear separation of concerns:

```
app/
├── domain/           # Business entities and interfaces
│   ├── entities/     # Core business models
│   └── interfaces/   # Abstract interfaces (repositories, services, cache)
├── application/      # Use cases and business logic
│   ├── usecases/     # Application use cases
│   ├── commands/     # Command handlers
│   └── services/     # Application services
├── adapters/         # External adapters
│   ├── api/          # FastAPI REST endpoints
│   ├── llm/          # LLM client adapter
│   ├── mongo/        # MongoDB repositories
│   ├── qdrant/       # Vector DB repositories
│   ├── s3/           # S3 storage adapter
│   └── search/       # Web search adapter
└── infrastructure/   # Infrastructure concerns
    └── di/           # Dependency injection (Dishka)

frontend/             # React frontend application
```

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Dependency Injection**: Dishka
- **Database**: MongoDB (via Beanie ODM)
- **Vector Store**: Qdrant
- **Cache**: Redis 7
- **File Storage**: MinIO (S3-compatible)
- **LLM**: Ollama (local inference)
- **Search**: SearXNG

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: TailwindCSS 4
- **UI Components**: Lucide React icons
- **Markdown**: react-markdown

## Prerequisites

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **8GB+ RAM** recommended for Ollama models

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/glebka1337/wfAI.git
cd wfAI
```

### 2. Configure Environment

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

**Environment Variables:**

```bash
# Backend API
BACKEND_URL=http://localhost:8000

# LLM Configuration
LLM_BASE_URL=http://ollama:11434/v1
LLM_API_KEY=ollama
DEFAULT_MODEL=llama3.2              # Default LLM model, but can be changed
EMBEDDING_MODEL=nomic-embed-text    # Embedding model for vectors

# MinIO (S3 Storage)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
S3_ENDPOINT_URL=http://minio:9000
S3_PUBLIC_URL=http://localhost:9000
S3_BUCKET_NAME=waifu-icons
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
```

### 3. Start the Application

```bash
docker compose up -d --build
```

This will start all services:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001
- **SearXNG**: http://localhost:8080

**First Launch**: The application will automatically pull the required Ollama models (`llama3.2` and `nomic-embed-text`). This may take 5-15 minutes depending on your internet connection.

### 4. Access the Application

Open your browser and navigate to:
- **Main Application**: http://localhost:5173

## Usage

### Chat Interface
1. Type your message in the input field
2. Press Enter or click Send
3. Toggle web search with the search button for enhanced responses
4. Regenerate responses by hovering over AI messages

### Persona Management
1. Open Settings (gear icon in sidebar)
2. Navigate to "Persona & Identity" tab
3. Customize AI name, icon, and personality traits
4. Changes apply immediately to new conversations

### Session Management
- All conversations are automatically saved
- Access previous sessions from the sidebar
- Delete individual sessions via the delete button
- Start new conversations with the "New Chat" button

## Development

### Running Locally (Without Docker)

**Backend:**
```bash
cd wfAI
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Project Structure

```
wfAI/
├── app/                    # Backend application
│   ├── domain/             # Domain layer (entities, interfaces)
│   ├── application/        # Application layer (use cases)
│   ├── adapters/           # Adapters layer (API, DB, external services)
│   ├── infrastructure/     # Infrastructure (DI, caching)
│   ├── core/               # Configuration
│   └── main.py             # Application entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # React context providers
│   │   ├── api/            # API client
│   │   └── App.jsx         # Main app component
│   └── package.json
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Backend container
├── requirements.txt        # Python dependencies
└── .env.example            # Environment template
```

## Docker Services

The application runs 8 Docker services:

1. **frontend**: React application (port 5173)
2. **app**: FastAPI backend (port 8000)
3. **searxng**: Web search engine (port 8080)
4. **ollama**: LLM inference server (port 11434)
5. **ollama-puller**: Automated model downloader
6. **qdrant**: Vector database (internal)
7. **mongo**: Document database (internal)
8. **minio**: S3-compatible object storage (ports 9000, 9001)
9. **redis**: Cache layer (port 6379)

## Data Persistence

All data is persisted in Docker volumes:
- `mongo_data`: Chat sessions, user profiles, personas
- `qdrant_data`: Vector embeddings and memories
- `ollama_data`: Downloaded LLM models
- `minio_data`: Uploaded persona icons
- `redis_data`: Cached data

## Troubleshooting

### Models Not Downloading
```bash
# Check Ollama service logs
docker logs waifu_ollama

# Manually pull models
docker exec -it waifu_ollama ollama pull llama3.2
docker exec -it waifu_ollama ollama pull nomic-embed-text
```

### Backend Connection Issues
```bash
# Check backend logs
docker logs waifu_backend

# Verify all services are healthy
docker compose ps
```

### Database Issues
```bash
# Restart MongoDB
docker compose restart mongo

# View MongoDB logs
docker logs waifu_mongo
```

### Port Conflicts
If ports 5173, 8000, 9000, or 11434 are already in use, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "NEW_PORT:5173"  # Change NEW_PORT to an available port
```

### Clear All Data
```bash
# Stop and remove all containers and volumes
docker compose down -v

# Restart fresh
docker compose up -d --build
```

## Cache Strategy

The application uses Redis for caching:
- **Session data**: Frequently accessed sessions cached with TTL
- **Search results**: Web search results cached to reduce API calls
- **User profiles**: Profile and persona data cached for fast access
- **Vector search**: Recent memory searches cached temporarily

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Follow the clean architecture principles
2. Use dependency injection via Dishka
3. Add type hints to all functions
4. Write docstrings for public methods
5. Test changes thoroughly

## License

This project is licensed under the MIT License.

## Acknowledgments

- **Ollama** for local LLM inference
- **SearXNG** for privacy-respecting web search
- **Qdrant** for vector similarity search
- **FastAPI** for the excellent Python framework
- **React** and **TailwindCSS** for the modern frontend

---

**Made with for AI enthusiasts**
