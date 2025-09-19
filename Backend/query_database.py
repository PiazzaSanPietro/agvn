#!/usr/bin/env python3
"""
Query utility for the SYSE cutted_script database
Usage: python query_database.py [command] [options]
"""
import sys
import argparse
from database_manager import DatabaseManager

def show_stats(db: DatabaseManager):
    """Display database statistics"""
    stats = db.get_database_stats()
    print("=== Database Statistics ===")
    print(f"Total chapters: {stats['total_chapters']}")
    print(f"Total scripts: {stats['total_scripts']}")
    print(f"Date range: {stats['earliest_chapter']} to {stats['latest_chapter']}")
    print()

def list_chapters(db: DatabaseManager, limit: int = None):
    """List all chapters"""
    chapters = db.get_all_chapters()
    if limit:
        chapters = chapters[:limit]

    print("=== Chapters ===")
    for chapter in chapters:
        print(f"ID: {chapter['id']}")
        print(f"Background: {chapter['scene_background']}")
        print(f"Scripts: {len(chapter['scripts'])}")
        print(f"Created: {chapter['created_at']}")
        print(f"First line: {chapter['scripts'][0]['role']}: {chapter['scripts'][0]['script'][:100]}...")
        print("-" * 50)

def show_chapter(db: DatabaseManager, chapter_id: int):
    """Show detailed chapter information"""
    chapter = db.get_chapter(chapter_id)
    if not chapter:
        print(f"Chapter {chapter_id} not found")
        return

    print(f"=== Chapter {chapter['id']} ===")
    print(f"Background: {chapter['scene_background']}")
    print(f"Created: {chapter['created_at']}")
    print(f"Scripts: {len(chapter['scripts'])}")
    print("\n=== Scripts ===")

    for i, script in enumerate(chapter['scripts'], 1):
        print(f"{i:2d}. {script['role']} ({script['emotion']})")
        print(f"    {script['script']}")
        print()

def search_character(db: DatabaseManager, character: str):
    """Search scripts by character name"""
    results = db.search_scripts_by_role(character)

    print(f"=== Scripts for '{character}' ===")
    print(f"Found {len(results)} scripts")
    print()

    current_chapter = None
    for result in results:
        if result['chapter_id'] != current_chapter:
            current_chapter = result['chapter_id']
            print(f"--- Chapter {current_chapter} ({result['scene_background']}) ---")

        print(f"{result['role']} ({result['emotion']}):")
        print(f"  {result['script']}")
        print()

def export_data(db: DatabaseManager, output_file: str):
    """Export database to JSON"""
    db.export_to_json(output_file)
    print(f"Database exported to {output_file}")

def show_concatenated_scripts(db: DatabaseManager, limit_chars: int = None):
    """Display concatenated scripts from all chapters"""
    try:
        result = db.get_all_scripts_concatenated()

        print("=== Concatenated Scripts ===")
        print(f"Total length: {len(result)} characters")
        print(f"Number of script lines: {len(result.splitlines())}")
        print()

        if limit_chars and len(result) > limit_chars:
            print(f"=== First {limit_chars} characters ===")
            print(result[:limit_chars])
            print("...")
        else:
            print("=== Complete Scripts ===")
            print(result)

    except Exception as e:
        print(f"Error retrieving concatenated scripts: {e}")

def clear_database(db: DatabaseManager):
    """Clear the database completely, including AUTOINCREMENT values"""
    print("⚠️  WARNING: This will permanently delete ALL data from the database!")
    print("This action cannot be undone.")
    print()

    confirm = input("Type 'CLEAR' to confirm database clear: ").strip()

    if confirm == 'CLEAR':
        try:
            success = db.clear_database()
            if success:
                print("✅ Database cleared successfully!")
                print("- All chapters and scripts deleted")
                print("- AUTOINCREMENT counters reset to 1")
                print("- Database vacuumed and reorganized")
            else:
                print("❌ Database clear failed - check logs for details")
        except Exception as e:
            print(f"❌ Error during database clear: {e}")
    else:
        print("Database clear cancelled.")

def main():
    parser = argparse.ArgumentParser(description="Query SYSE cutted_script database")
    parser.add_argument('command', choices=['stats', 'list', 'show', 'search', 'export', 'concat', 'clear'],
                       help='Command to execute')
    parser.add_argument('--chapter-id', type=int, help='Chapter ID for show command')
    parser.add_argument('--character', type=str, help='Character name for search command')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--output', type=str, help='Output file for export command')

    if len(sys.argv) == 1:
        # Interactive mode if no arguments
        db = DatabaseManager()

        while True:
            print("\n=== SYSE Database Query Tool ===")
            print("1. Show statistics")
            print("2. List chapters")
            print("3. Show specific chapter")
            print("4. Search by character")
            print("5. Export database")
            print("6. Show concatenated scripts")
            print("7. Clear database (⚠️  DANGER)")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == '1':
                show_stats(db)
            elif choice == '2':
                limit = input("Limit results (press Enter for all): ").strip()
                limit = int(limit) if limit else None
                list_chapters(db, limit)
            elif choice == '3':
                chapter_id = input("Enter chapter ID: ").strip()
                try:
                    chapter_id = int(chapter_id)
                    show_chapter(db, chapter_id)
                except ValueError:
                    print("Invalid chapter ID")
            elif choice == '4':
                character = input("Enter character name: ").strip()
                if character:
                    search_character(db, character)
            elif choice == '5':
                output_file = input("Enter output filename: ").strip()
                if output_file:
                    export_data(db, output_file)
            elif choice == '6':
                limit = input("Limit characters (press Enter for all): ").strip()
                limit = int(limit) if limit else None
                show_concatenated_scripts(db, limit)
            elif choice == '7':
                clear_database(db)
            elif choice == '8':
                print("Goodbye!")
                break
            else:
                print("Invalid choice")
    else:
        # Command-line mode
        args = parser.parse_args()
        db = DatabaseManager()

        if args.command == 'stats':
            show_stats(db)
        elif args.command == 'list':
            list_chapters(db, args.limit)
        elif args.command == 'show':
            if not args.chapter_id:
                print("Error: --chapter-id required for show command")
                return
            show_chapter(db, args.chapter_id)
        elif args.command == 'search':
            if not args.character:
                print("Error: --character required for search command")
                return
            search_character(db, args.character)
        elif args.command == 'export':
            output_file = args.output or 'database_export.json'
            export_data(db, output_file)
        elif args.command == 'concat':
            limit = args.limit
            show_concatenated_scripts(db, limit)
        elif args.command == 'clear':
            clear_database(db)

if __name__ == "__main__":
    main()