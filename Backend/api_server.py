from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generate_script import GenerateScript
import sys
import threading
import time
import webbrowser
from pathlib import Path

# --- Pydantic model for request body ---
class StoryLine(BaseModel):
    """Request model for receiving text prompts."""
    line: str

# --- FastAPI application initialization ---
app = FastAPI(
    title="story gen api",
    description="make story",
    version="2.0.0",
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # React dev server and API server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files from React build
def get_frontend_build_path():
    """Get the correct path to frontend build directory, whether running as script or executable."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return Path(sys._MEIPASS) / "frontend" / "build"
    else:
        # Running as script
        return Path(__file__).parent.parent / "frontend" / "build"

frontend_build_path = get_frontend_build_path()

# Check if static and assets directories exist before mounting
if (frontend_build_path / "static").exists():
    app.mount("/static", StaticFiles(directory=str(frontend_build_path / "static")), name="static")

if (frontend_build_path / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_build_path / "assets")), name="assets")

# Initialize GenerateScript service
try:
    generate_script_service = GenerateScript()
except ValueError:
    # Exit if service cannot be initialized
    print("Failed to initialize GenerateScript service. Check your API key configuration.")
    sys.exit(1)

# --- API endpoints ---
@app.post("/generate script", summary="Generate script from prompt")
async def generate_script(index: int):
    """Generates a script based on the provided prompt and ws index using Gemini API."""
    try:
        result = generate_script_service.generate_script(index)
        return result
    except Exception as e:
        # Handle errors that may occur during API calls
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate content from Gemini API.")

# --- Health check endpoint ---
@app.get("/api/health", summary="Health check")
def read_root():
    """Simple endpoint to check if the server is running."""
    return {"status": "ok"}

# --- Serve React frontend for all other routes (SPA routing) ---
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve React app for all non-API routes to support client-side routing."""
    # Handle root path
    if full_path == "" or full_path == "/":
        return FileResponse(str(frontend_build_path / "index.html"))

    # Return index.html for any path that's not an API endpoint
    if not full_path.startswith(("generate", "static", "assets", "api")):
        return FileResponse(str(frontend_build_path / "index.html"))

    # If it's an unmatched API-like path, return 404
    raise HTTPException(status_code=404, detail="Not found")

def open_browser():
    """Open the browser to the frontend after a delay."""
    time.sleep(2)  # Wait 2 seconds for server to fully start
    try:
        webbrowser.open("http://localhost:8000")
        print("Browser opened automatically at http://localhost:8000")
    except Exception as e:
        print(f"Could not automatically open browser: {e}")
        print("Please manually open: http://localhost:8000")

# --- Main execution ---
if __name__ == "__main__":
    import uvicorn

    # Start browser opening in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    print("Starting server... Browser will open automatically in 2 seconds.")
    uvicorn.run(app, host="0.0.0.0", port=8000)