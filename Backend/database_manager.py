import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from tool.logmaker import log

class DatabaseManager:
    """Database manager for cutted_script data storage and retrieval"""

    def __init__(self, db_path: str = "data/scripts.db"):
        """Initialize database manager with database path"""
        self.db_path = Path(__file__).parent / db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_database()

    def initialize_database(self):
        """Create database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Create chapters table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chapters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scene_background TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Create scripts table with foreign key to chapters
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scripts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chapter_id INTEGER NOT NULL,
                        role TEXT NOT NULL,
                        emotion TEXT NOT NULL,
                        script TEXT NOT NULL,
                        order_index INTEGER NOT NULL,
                        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
                    )
                """)

                conn.commit()
                log('database_manager', 'Database tables initialized successfully')

        except Exception as e:
            log('database_manager', f'Error initializing database: {e}')
            raise e

    def save_chapter(self, chapter_data: Dict) -> int:
        """Save chapter data to database and return chapter ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Handle enum values - convert to string if needed
                scene_background = chapter_data.get('scene_background', 'unknown')
                if hasattr(scene_background, 'value'):  # Handle enum objects
                    scene_background = scene_background.value

                # Insert chapter record
                cursor.execute(
                    "INSERT INTO chapters (scene_background) VALUES (?)",
                    (scene_background,)
                )

                chapter_id = cursor.lastrowid

                # Insert script records
                scripts = chapter_data.get('scripts', [])
                for idx, script in enumerate(scripts):
                    # Handle enum values for emotion
                    emotion = script['emotion']
                    if hasattr(emotion, 'value'):  # Handle enum objects
                        emotion = emotion.value

                    cursor.execute(
                        "INSERT INTO scripts (chapter_id, role, emotion, script, order_index) VALUES (?, ?, ?, ?, ?)",
                        (chapter_id, script['role'], emotion, script['script'], idx)
                    )

                conn.commit()
                log('database_manager', f'Chapter saved with ID: {chapter_id}, {len(scripts)} scripts')
                return chapter_id

        except Exception as e:
            log('database_manager', f'Error saving chapter: {e}')
            raise e

    def get_chapter(self, chapter_id: int) -> Optional[Dict]:
        """Retrieve chapter data by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get chapter info
                cursor.execute(
                    "SELECT id, scene_background, created_at FROM chapters WHERE id = ?",
                    (chapter_id,)
                )
                chapter_row = cursor.fetchone()

                if not chapter_row:
                    return None

                # Get scripts for this chapter
                cursor.execute(
                    "SELECT role, emotion, script FROM scripts WHERE chapter_id = ? ORDER BY order_index",
                    (chapter_id,)
                )
                script_rows = cursor.fetchall()

                return {
                    'id': chapter_row[0],
                    'scene_background': chapter_row[1],
                    'created_at': chapter_row[2],
                    'scripts': [
                        {'role': row[0], 'emotion': row[1], 'script': row[2]}
                        for row in script_rows
                    ]
                }

        except Exception as e:
            log('database_manager', f'Error retrieving chapter {chapter_id}: {e}')
            raise e

    def get_all_chapters(self) -> List[Dict]:
        """Retrieve all chapters with their scripts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM chapters ORDER BY created_at")
                chapter_ids = [row[0] for row in cursor.fetchall()]

                return [self.get_chapter(chapter_id) for chapter_id in chapter_ids]

        except Exception as e:
            log('database_manager', f'Error retrieving all chapters: {e}')
            raise e

    def search_scripts_by_role(self, role: str) -> List[Dict]:
        """Search scripts by character role"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT c.id, c.scene_background, c.created_at, s.role, s.emotion, s.script, s.order_index
                    FROM chapters c
                    JOIN scripts s ON c.id = s.chapter_id
                    WHERE s.role LIKE ?
                    ORDER BY c.created_at, s.order_index
                """, (f'%{role}%',))

                results = []
                for row in cursor.fetchall():
                    results.append({
                        'chapter_id': row[0],
                        'scene_background': row[1],
                        'created_at': row[2],
                        'role': row[3],
                        'emotion': row[4],
                        'script': row[5],
                        'order_index': row[6]
                    })

                return results

        except Exception as e:
            log('database_manager', f'Error searching scripts by role {role}: {e}')
            raise e

    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM chapters")
                chapter_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM scripts")
                script_count = cursor.fetchone()[0]

                cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM chapters")
                date_range = cursor.fetchone()

                return {
                    'total_chapters': chapter_count,
                    'total_scripts': script_count,
                    'earliest_chapter': date_range[0],
                    'latest_chapter': date_range[1]
                }

        except Exception as e:
            log('database_manager', f'Error getting database stats: {e}')
            raise e

    def load_cutted_script_from_logs(self, log_file_path: str) -> int:
        """Load existing cutted_script data from log files into database"""
        try:
            log_path = Path(log_file_path)
            if not log_path.exists():
                log('database_manager', f'Log file not found: {log_file_path}')
                return 0

            loaded_count = 0
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

                # Try to parse as JSON (from response_text.log)
                try:
                    chapter_data = json.loads(content)
                    if 'scripts' in chapter_data:
                        chapter_id = self.save_chapter(chapter_data)
                        loaded_count = 1
                        log('database_manager', f'Loaded chapter from JSON log: {chapter_id}')
                except json.JSONDecodeError:
                    # Parse as plain text format (from cutted_script_str.log)
                    lines = content.split('\n')
                    scripts = []

                    for line in lines:
                        if ':' in line:
                            role, script = line.split(':', 1)
                            scripts.append({
                                'role': role.strip(),
                                'emotion': 'neutral',  # Default emotion for log imports
                                'script': script.strip()
                            })

                    if scripts:
                        chapter_data = {
                            'scene_background': 'unknown',  # Default background for log imports
                            'scripts': scripts
                        }
                        chapter_id = self.save_chapter(chapter_data)
                        loaded_count = 1
                        log('database_manager', f'Loaded chapter from text log: {chapter_id}')

            return loaded_count

        except Exception as e:
            log('database_manager', f'Error loading from log file {log_file_path}: {e}')
            raise e

    def get_all_scripts_concatenated(self) -> str:
        """Retrieve all script content and concatenate into a single string.

        Fetches script content for all chapters, filtering to include only
        role and script data fields, then concatenates into a single string.

        Returns:
            str: Concatenated script data with format 'Role: Script' per line
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Query to get all scripts ordered by chapter creation time and script order
                cursor.execute("""
                    SELECT s.role, s.script
                    FROM chapters c
                    JOIN scripts s ON c.id = s.chapter_id
                    ORDER BY c.created_at, s.order_index
                """)

                script_rows = cursor.fetchall()

                # Format and concatenate scripts
                concatenated_scripts = []
                for role, script in script_rows:
                    concatenated_scripts.append(f"{role}: {script}")

                result = "\n".join(concatenated_scripts)

                log('database_manager', f'Retrieved and concatenated {len(script_rows)} scripts from database')
                return "Previous story:\n" + result

        except Exception as e:
            log('database_manager', f'Error retrieving concatenated scripts: {e}')
            raise e

    def clear_database(self) -> bool:
        """Clear all data from the database and reset AUTOINCREMENT values.

        This function will:
        1. Delete all data from both tables
        2. Reset AUTOINCREMENT counters to start from 1
        3. Vacuum the database to reclaim space

        Returns:
            bool: True if clear was successful, False otherwise
        """
        try:
            # First phase: Delete data and reset sequences within transaction
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Delete all data from scripts table first (due to foreign key constraints)
                cursor.execute("DELETE FROM scripts")
                log('database_manager', 'Cleared all scripts from database')

                # Delete all data from chapters table
                cursor.execute("DELETE FROM chapters")
                log('database_manager', 'Cleared all chapters from database')

                # Reset AUTOINCREMENT sequences by deleting from sqlite_sequence table
                cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('chapters', 'scripts')")
                log('database_manager', 'Reset AUTOINCREMENT sequences for chapters and scripts tables')

                conn.commit()

                # Verify clear by checking counts
                cursor.execute("SELECT COUNT(*) FROM chapters")
                chapter_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM scripts")
                script_count = cursor.fetchone()[0]

                if chapter_count != 0 or script_count != 0:
                    log('database_manager', f'Warning: Clear incomplete - chapters: {chapter_count}, scripts: {script_count}')
                    return False

            # Second phase: VACUUM database outside of transaction
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("VACUUM")
                log('database_manager', 'Database vacuumed and reorganized')

            log('database_manager', 'Database cleared successfully - all tables empty and AUTOINCREMENT reset')
            return True

        except Exception as e:
            log('database_manager', f'Error clearing database: {e}')
            raise e

    def export_to_json(self, output_file: str):
        """Export all database contents to JSON file"""
        try:
            chapters = self.get_all_chapters()

            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_chapters': len(chapters),
                'chapters': chapters
            }

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            log('database_manager', f'Database exported to {output_file}')

        except Exception as e:
            log('database_manager', f'Error exporting database: {e}')
            raise e


def main():
    """Main function for testing database manager"""
    db_manager = DatabaseManager()

    # Display database stats
    stats = db_manager.get_database_stats()
    print(f"Database Statistics:")
    print(f"Total chapters: {stats['total_chapters']}")
    print(f"Total scripts: {stats['total_scripts']}")
    print(f"Date range: {stats['earliest_chapter']} to {stats['latest_chapter']}")

    # Load from existing log files if they exist
    log_files = [
        "logs/response_text.log",
        "logs/cutted_script_str.log"
    ]

    for log_file in log_files:
        log_path = Path(__file__).parent / log_file
        if log_path.exists():
            try:
                loaded = db_manager.load_cutted_script_from_logs(str(log_path))
                if loaded > 0:
                    print(f"Loaded {loaded} chapter(s) from {log_file}")
            except Exception as e:
                print(f"Error loading from {log_file}: {e}")


if __name__ == "__main__":
    main()