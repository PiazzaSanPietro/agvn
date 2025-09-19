import enum
import os
import sys
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import logging module
from tool.logmaker import log
# Import character name normalization module
from tool.character_normalizer import normalize_character_name
# Import database manager
from database_manager import DatabaseManager

# Load environment variables from .env file
load_dotenv()

# --- Enum defining emotion states ---
class Emotion(enum.Enum):
    # Base Expressions
    NEUTRAL = 'neutral'      # Calm/expressionless
    HAPPY = 'happy'        # Happy/joyful
    SAD = 'sad'            # Sadness
    ANGRY = 'angry'          # Angry
    SURPRISED = 'surprised'    # Surprised/shocked
    SHY = 'shy'                  # Shy


# --- Script model definition ---
class Script(BaseModel):
    role: str
    emotion: Emotion
    script: str

class Background(enum.Enum):
    Classroom_Day = 'Classroom_Day'
    Classroom_Sunset = 'Classroom_Sunset'
    School_Hallway_Day = 'School_Hallway_Day'
    School_Rooftop = 'School_Rooftop'
    Protagonist_Room = 'Protagonist_Room'
    Cafe_Interior = 'Cafe_Interior'
    Park = 'Park'
    Schoolyard = 'Schoolyard'

class Chapter(BaseModel):
    """Add background information"""
    scene_background: Background
    scripts: list[Script]

def get_prompts_path():
    """Get the correct path to prompts directory, whether running as script or executable."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return Path(sys._MEIPASS) / "Backend" / "prompts"
    else:
        # Running as script
        return Path(__file__).parent / "prompts"

class GenerateScript:
    """Service class for handling Gemini API interactions"""
    
    def __init__(self):
        """Initialize Gemini client with API key and database manager"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables.")
            # Create Google AI client instance
            self.client = genai.Client(api_key=api_key)
            # Initialize database manager
            self.db_manager = DatabaseManager()
        except ValueError as e:
            print(f"Error: {e}")
            raise e
    
    def generate_script(self,index: int = 0):

        try:

            # Read base world prompt from file
            base_world_prompt_path = get_prompts_path() / "base_world.prompt"
            try:
                with open(base_world_prompt_path, 'r', encoding='utf-8') as f:
                    base_world_prompt = f.read()
            except FileNotFoundError:
                log('story_generation_workflow', f'Warning: base_world.prompt file not found at {base_world_prompt_path}')
                base_world_prompt = ""
            except Exception as e:
                log('story_generation_workflow', f'Error reading base_world.prompt: {e}')
                base_world_prompt = ""

            if index > 1:
                all_scripts_concatenated = self.db_manager.get_all_scripts_concatenated()
            else:
                all_scripts_concatenated = ""
                self.db_manager.clear_database()  # Clear database for new story

            prompt = f"{base_world_prompt}\n{all_scripts_concatenated}\n---\nBased on the characters and world-building provided above, please write a script for a visual novel dating simulation. The script should be one chapter long and consist of the narrator's descriptions and the characters' dialogue. 한국어로 작성되어야 합니다."

            log('chat_context', prompt)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Chapter,
                    max_output_tokens=35500,
                    temperature=1,
                ),
            )

            chapter: Chapter = response.parsed

            # Normalize character names in all scripts
            for script in chapter.scripts:
                script.role = normalize_character_name(script.role)

            cutted_script = [f"{line.role}: {line.script}" for line in chapter.scripts]
            cutted_script_str = "\n".join(cutted_script)
            log('cutted_script_str', cutted_script_str)
            log('response_text', response.text)

            # Convert chapter to dictionary for database storage
            chapter_data = chapter.model_dump()

            # Save to database
            try:
                chapter_id = self.db_manager.save_chapter(chapter_data)
                log('story_generation_workflow', f'Chapter saved to database with ID: {chapter_id}')
            except Exception as db_error:
                log('story_generation_workflow', f'Warning: Failed to save chapter to database: {db_error}')
                # Continue execution even if database save fails

            # Return chapter as JSON object
            return chapter_data

        except Exception as e:
            # Handle errors that may occur during API calls
            print(f"An error occurred during story generation: {e}")
            raise e