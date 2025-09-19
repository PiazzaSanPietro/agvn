# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a story generation application with a Python FastAPI backend and React frontend. The system uses Google's Generative AI to create interactive stories with character emotions and scene backgrounds.

### Backend (Python/FastAPI)
- **Main API Server**: `Backend/api_server.py` - FastAPI server that serves both API endpoints and static React frontend
- **Story Generation**: `Backend/generate_script.py` - Core story generation logic using Google GenAI
- **Database Management**: `Backend/database_manager.py` - SQLite database for story chapters and dialogues
- **Character Processing**: `Backend/tool/character_normalizer.py` - Normalizes character names for consistency
- **Logging**: `Backend/tool/logmaker.py` - Centralized logging utility

### Frontend (React)
- **Main App**: `frontend/src/App.js` - Root component managing game state and screens
- **Components**: `frontend/src/components/` - React components for different screens
- **API Service**: `frontend/src/services/apiService.js` - Frontend API communication layer

## Development Commands

### Backend (Run from project root)
```bash
# Start the API server (serves both API and frontend)
cd Backend && python api_server.py

# Query existing database content
cd Backend && python query_database.py

# Run character normalizer tests
cd Backend && python test_character_normalizer.py
```

### Frontend Development
```bash
# Install dependencies
cd frontend && npm install

# Start development server (for frontend-only development)
cd frontend && npm start

# Build for production
cd frontend && npm run build

# Run tests
cd frontend && npm test
```

## Key Architecture Notes

### Unified Server Architecture
The FastAPI server (`Backend/api_server.py`) serves both:
- API endpoints at `/generate script` and `/continue`
- Static React frontend from `frontend/build/`
- This allows running the entire application from a single Python process

### Story Generation Flow
1. User provides API key and starts game
2. Frontend calls `/generate script?index=1` to create initial story
3. Story generation uses Google GenAI with custom prompts from `Backend/prompt/` and `Backend/prompts/`
4. Generated content includes dialogue, emotions, and scene backgrounds
5. Data is stored in SQLite database via `DatabaseManager`
6. Character names are normalized using `character_normalizer.py`

### Database Schema
- **chapters**: Story chapters with scene backgrounds
- **dialogues**: Character dialogues with emotions and metadata
- Uses SQLite database stored in `Backend/data/scripts.db`

### Environment Configuration
- Requires `GOOGLE_API_KEY` in `.env` file for GenAI access
- API key can also be provided through frontend interface

### Character Emotion System
The application includes a comprehensive emotion system defined in `generate_script.py`:
- Base expressions: neutral, smile, laugh, ecstatic, gloomy, crying, sobbing
- Complex emotions: angry, surprised, confused, shy, etc.
- Character names are normalized to ensure consistency across dialogue generation