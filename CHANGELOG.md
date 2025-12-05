# Changelog

All notable changes to the Downloads Organizer project.

## [1.1.0] - 2025-12-05

### Added - Polish Improvements
- **Date-based organization**: New `--by-date` flag organizes files into year/month subfolders based on modification date
- **Configurable categories**: Support for custom categories via `organize_config.json` in the target folder
- **Undo functionality**: New `--undo` flag to reverse the last organization operation
- **Operation history**: Automatic tracking of file moves in `.organize_history.json` (keeps last 100 operations)
- **Music category**: Added support for audio files (mp3, wav, flac, aac, ogg, m4a, wma)
- **Code category**: Added support for source code files (py, js, java, cpp, c, h, cs, php, rb, go, rs, ts, html, css)
- **Example config file**: `organize_config.example.json` showing how to customize categories

### Changed
- Enhanced logging to show relative paths for better readability
- Config and history files are now automatically skipped during organization
- Categories are now loaded dynamically (can be overridden by config file)
- Improved help text with examples for all new features

### Technical
- Added `load_config()` function to read custom categories
- Added `save_history()` function to track operations
- Added `undo_last_operation()` function to reverse changes
- Updated `organize_downloads()` to support date-based organization
- All new features are optional and don't affect default behavior

## [1.0.0] - 2025-12-05

### Initial Release
- Cross-platform Downloads folder detection (Windows, macOS, Linux)
- Automatic file categorization by extension
- 5 default categories: Images, Documents, Videos, Archives, Installers
- Dry-run mode for safe testing
- Comprehensive logging to organize.log
- Duplicate filename handling
- System/hidden file protection
- Custom path support via `--path` argument
- Clean, well-commented code with small functions
- Complete documentation and README
