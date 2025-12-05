#!/usr/bin/env python3
"""
Downloads Folder Organizer
Automatically organizes files in your Downloads folder into categorized subfolders.
"""

import os
import sys
import shutil
import logging
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse


# Default file extension categories
DEFAULT_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico'],
    'Documents': ['.pdf', '.docx', '.xlsx', '.txt', '.pptx', '.doc', '.xls', '.ppt', '.odt', '.csv'],
    'Videos': ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv', '.webm'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Installers': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.pkg', '.apk'],
    'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.ts', '.html', '.css']
}

# Global variable to hold active categories (can be overridden by config)
CATEGORIES = DEFAULT_CATEGORIES.copy()


def get_downloads_folder():
    """
    Detect the user's Downloads folder based on the operating system.
    Returns the path to the Downloads folder.
    """
    home = Path.home()
    
    # Try common Downloads folder locations
    if sys.platform == 'win32':
        downloads = home / 'Downloads'
    elif sys.platform == 'darwin':  # macOS
        downloads = home / 'Downloads'
    else:  # Linux and others
        downloads = home / 'Downloads'
    
    return downloads


def setup_logging(downloads_path):
    """
    Set up logging to both console and file.
    """
    log_file = downloads_path / 'organize.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def load_config(downloads_path):
    """
    Load custom categories from config.json if it exists.
    Returns custom categories or None if config doesn't exist.
    """
    config_file = downloads_path / 'organize_config.json'
    
    if not config_file.exists():
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('categories', None)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Could not load config file: {e}")
        return None


def get_category(file_extension):
    """
    Determine the category for a file based on its extension.
    Returns the category name or None if no match.
    """
    file_extension = file_extension.lower()
    
    for category, extensions in CATEGORIES.items():
        if file_extension in extensions:
            return category
    
    return None


def is_system_or_hidden(file_path):
    """
    Check if a file is a system or hidden file.
    """
    # Check if file starts with dot (hidden on Unix-like systems)
    if file_path.name.startswith('.'):
        return True
    
    # Check Windows hidden attribute
    if sys.platform == 'win32':
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
            # FILE_ATTRIBUTE_HIDDEN = 0x2
            if attrs != -1 and attrs & 0x2:
                return True
        except Exception:
            pass
    
    return False


def save_history(downloads_path, history_entry):
    """
    Save file move operation to history for undo functionality.
    """
    history_file = downloads_path / '.organize_history.json'
    
    try:
        # Load existing history
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {'operations': []}
        
        # Add new entry
        history['operations'].append(history_entry)
        
        # Keep only last 100 operations to prevent file from growing too large
        history['operations'] = history['operations'][-100:]
        
        # Save history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Could not save history: {e}")


def organize_downloads(downloads_path, dry_run=False, by_date=False):
    """
    Main function to organize files in the Downloads folder.
    
    Args:
        downloads_path: Path to the folder to organize
        dry_run: If True, only preview changes without moving files
        by_date: If True, organize into year/month subfolders
    """
    logger = logging.getLogger(__name__)
    
    # Statistics
    stats = defaultdict(int)
    skipped = 0
    
    # Track operations for history
    operations = []
    
    logger.info(f"Starting organization of: {downloads_path}")
    logger.info(f"Dry run mode: {dry_run}")
    if by_date:
        logger.info(f"Date-based organization: enabled")
    logger.info("-" * 60)
    
    # Get all files in Downloads (non-recursive)
    try:
        files = [f for f in downloads_path.iterdir() if f.is_file()]
    except PermissionError:
        logger.error(f"Permission denied accessing: {downloads_path}")
        return
    
    # Record session start time
    session_timestamp = datetime.now().isoformat()
    
    for file_path in files:
        try:
            # Skip system/hidden files
            if is_system_or_hidden(file_path):
                logger.debug(f"Skipping hidden/system file: {file_path.name}")
                skipped += 1
                continue
            
            # Skip the log file, config, and history files
            if file_path.name in ['organize.log', 'organize_config.json', '.organize_history.json']:
                skipped += 1
                continue
            
            # Get file extension and category
            file_extension = file_path.suffix
            category = get_category(file_extension)
            
            if category is None:
                logger.info(f"No category for: {file_path.name} (extension: {file_extension})")
                skipped += 1
                continue
            
            # Create target folder (with optional date-based subfolder)
            if by_date:
                # Get file modification time
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                year = mod_time.strftime('%Y')
                month = mod_time.strftime('%B')  # Full month name
                target_folder = downloads_path / category / year / month
            else:
                target_folder = downloads_path / category
            
            if not dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)
            
            # Determine target path
            target_path = target_folder / file_path.name
            
            # Handle duplicate filenames
            counter = 1
            original_target = target_path
            while target_path.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = target_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            relative_target = target_path.relative_to(downloads_path)
            
            if dry_run:
                logger.info(f"[DRY RUN] Would move: {file_path.name} → {relative_target}")
            else:
                shutil.move(str(file_path), str(target_path))
                logger.info(f"Moved: {file_path.name} → {relative_target}")
                
                # Record operation for undo
                operations.append({
                    'timestamp': session_timestamp,
                    'source': str(file_path),
                    'destination': str(target_path),
                    'filename': file_path.name
                })
            
            stats[category] += 1
            
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            skipped += 1
    
    # Print summary
    logger.info("-" * 60)
    logger.info("SUMMARY:")
    logger.info(f"Total files processed: {sum(stats.values())}")
    
    for category, count in sorted(stats.items()):
        logger.info(f"  {category}: {count} files")
    
    logger.info(f"Files skipped: {skipped}")
    
    if dry_run:
        logger.info("\nThis was a dry run. No files were actually moved.")
    elif operations:
        # Save history for undo
        history_entry = {
            'timestamp': session_timestamp,
            'operations': operations
        }
        save_history(downloads_path, history_entry)


def undo_last_operation(downloads_path):
    """
    Undo the last organization operation.
    """
    logger = logging.getLogger(__name__)
    history_file = downloads_path / '.organize_history.json'
    
    if not history_file.exists():
        logger.error("No history file found. Nothing to undo.")
        return
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if not history.get('operations'):
            logger.error("No operations in history. Nothing to undo.")
            return
        
        # Get last operation
        last_session = history['operations'].pop()
        operations = last_session.get('operations', [])
        
        logger.info(f"Undoing operation from: {last_session['timestamp']}")
        logger.info(f"Moving {len(operations)} files back to original location...")
        logger.info("-" * 60)
        
        success_count = 0
        error_count = 0
        
        # Reverse the operations
        for op in reversed(operations):
            try:
                source = Path(op['destination'])
                dest = Path(op['source'])
                
                if source.exists():
                    shutil.move(str(source), str(dest))
                    logger.info(f"Restored: {op['filename']}")
                    success_count += 1
                else:
                    logger.warning(f"File not found, skipping: {op['filename']}")
                    error_count += 1
            except Exception as e:
                logger.error(f"Error restoring {op['filename']}: {e}")
                error_count += 1
        
        # Save updated history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
        
        logger.info("-" * 60)
        logger.info(f"Undo complete: {success_count} files restored, {error_count} errors")
        
    except Exception as e:
        logger.error(f"Error during undo: {e}")


def main():
    """
    Entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description='Organize your Downloads folder automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organize_downloads.py                      # Organize default Downloads folder
  python organize_downloads.py --dry-run            # Preview what would happen
  python organize_downloads.py --path /custom/path  # Organize custom folder
  python organize_downloads.py --by-date            # Organize into year/month subfolders
  python organize_downloads.py --undo               # Undo last organization
        """
    )
    
    parser.add_argument(
        '--path',
        type=str,
        help='Custom path to organize (default: system Downloads folder)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without actually moving files'
    )
    
    parser.add_argument(
        '--by-date',
        action='store_true',
        help='Organize files into year/month subfolders based on modification date'
    )
    
    parser.add_argument(
        '--undo',
        action='store_true',
        help='Undo the last organization operation'
    )
    
    args = parser.parse_args()
    
    # Determine Downloads folder
    if args.path:
        downloads_path = Path(args.path)
    else:
        downloads_path = get_downloads_folder()
    
    # Validate path
    if not downloads_path.exists():
        print(f"Error: Path does not exist: {downloads_path}")
        sys.exit(1)
    
    if not downloads_path.is_dir():
        print(f"Error: Path is not a directory: {downloads_path}")
        sys.exit(1)
    
    # Setup logging
    setup_logging(downloads_path)
    
    # Handle undo operation
    if args.undo:
        undo_last_operation(downloads_path)
        return
    
    # Load custom config if available
    global CATEGORIES
    custom_categories = load_config(downloads_path)
    if custom_categories:
        CATEGORIES = custom_categories
        logging.getLogger(__name__).info("Loaded custom categories from organize_config.json")
    
    # Run organization
    organize_downloads(downloads_path, dry_run=args.dry_run, by_date=args.by_date)


if __name__ == '__main__':
    main()
