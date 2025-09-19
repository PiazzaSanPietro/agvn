# Ai Generated Visual Novel

An interactive story generation application that creates dynamic narratives with character emotions and scene backgrounds using Google's Generative AI.

## Features

- **Interactive Story Generation**: AI-powered story creation with branching narratives
- **Character Emotion System**: Comprehensive emotion tracking with visual expressions
- **Dynamic Scene Backgrounds**: AI-generated scene descriptions for immersive storytelling
- **Character Consistency**: Automatic character name normalization across dialogues
- **Database Persistence**: SQLite storage for story chapters and character dialogues
- **Web Interface**: React frontend with intuitive game controls

## Tech Stack

### Backend
- **Python 3.x** with FastAPI
- **Google Generative AI** for story generation
- **SQLite** database for persistence
- **Uvicorn** ASGI server

### Frontend
- **React** with modern JavaScript
- **CSS3** for styling and animations
- **Fetch API** for backend communication

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Node.js and npm (for frontend development)
- Google API key for Generative AI

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agvn
   ```

2. **Set up the backend**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` file in the Backend directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

5. **Build the frontend**
   ```bash
   npm run build
   ```

### Running the Application

#### Production Mode (Recommended)
Run the unified server that serves both API and frontend:
```bash
cd Backend
python api_server.py
```
The application will be available at `http://localhost:8000`

#### Development Mode
For frontend development with hot reload:
```bash
# Terminal 1 - Backend API
cd Backend
python api_server.py

# Terminal 2 - Frontend development server
cd frontend
npm start
```
Frontend will be available at `http://localhost:3000`

## Usage

1. **Start the Application**: Launch the server and navigate to the web interface
2. **Enter API Key**: Provide your Google API key through the interface
3. **Begin Story**: Click "Start Game" to generate your first story chapter
4. **Continue Adventure**: Use "Continue" to progress through the narrative
5. **Explore**: Enjoy the AI-generated stories with dynamic characters and emotions

## Project Structure

```
agvn/
├── Backend/
│   ├── api_server.py          # Main FastAPI server
│   ├── generate_script.py     # Story generation logic
│   ├── database_manager.py    # Database operations
│   ├── prompt/                # Story generation prompts
│   ├── tool/
│   │   ├── character_normalizer.py  # Character name consistency
│   │   └── logmaker.py        # Logging utilities
│   └── data/                  # SQLite database storage
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── components/       # React components
│   │   └── services/         # API communication
│   └── build/                # Production build output
└── README.md
```

## API Endpoints

- `GET /` - Serves the React frontend
- `POST /generate script` - Generate new story chapter
- `POST /continue` - Continue existing story
- `GET /static/` - Static file serving

## Database Schema

The application uses SQLite with two main tables:
- **chapters**: Story chapters with scene backgrounds
- **dialogues**: Character dialogues with emotions and metadata

## Development Commands

### Backend Testing
```bash
cd Backend
python query_database.py           # Query database contents
python test_character_normalizer.py # Test character normalization
```

### Frontend Development
```bash
cd frontend
npm test        # Run tests
npm run build   # Build for production
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [GPL 3.0 License](LICENSE).

## Troubleshooting

### Common Issues

**"Missing Google API Key"**
- Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
- API key can also be entered through the web interface

**"Frontend not loading"**
- Make sure you've built the frontend with `npm run build`
- Check that the backend server is running on port 8000

**"Database errors"**
- The SQLite database will be created automatically on first run
- Check file permissions in the `Backend/data/` directory

## Support

For issues and questions, please open an issue on the GitHub repository.

## Notice

Some of the images and source code in this project were created using generative AI.