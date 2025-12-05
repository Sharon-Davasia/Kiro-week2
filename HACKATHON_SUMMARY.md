# AI for Bharat – Kiro Week 2 Challenge Submission

## Project: Downloads Folder Organizer

### Challenge Theme: Lazy Automation

### Problem Statement
Downloads folders become messy quickly with mixed file types, making it hard to find what you need. Manual organization is tedious and time-consuming.

### Solution
A Python script that automatically organizes Downloads folders by categorizing files into subfolders based on their type, with advanced features for power users.

---

## Core Features (Required)

✅ **Cross-platform detection** - Automatically finds Downloads folder on Windows, macOS, Linux  
✅ **Smart categorization** - 7 categories with 50+ file extensions  
✅ **Safe operation** - Skips system/hidden files, handles duplicates  
✅ **Dry-run mode** - Preview changes before applying  
✅ **Comprehensive logging** - All actions logged to organize.log  
✅ **Error handling** - Graceful error handling with detailed summary  
✅ **Custom paths** - Organize any folder, not just Downloads  

---

## Polish Features (Improvements)

### 1. Date-Based Organization 📅
```bash
python organize_downloads.py --by-date
```
- Organizes files into `Category/Year/Month/` structure
- Based on file modification date
- Perfect for archival and time-based retrieval

### 2. Configurable Categories ⚙️
- Custom categories via `organize_config.json`
- No code changes needed
- Example config provided
- Automatically detected and loaded

### 3. Undo Functionality ↩️
```bash
python organize_downloads.py --undo
```
- Reverses last organization operation
- Tracks up to 100 operations
- Moves files back to original locations
- Safe recovery from mistakes

---

## Technical Highlights

### Code Quality
- **Clean architecture**: Small, focused functions
- **Well-commented**: Every function documented
- **Type hints ready**: Easy to add type annotations
- **Error resilient**: Comprehensive exception handling
- **No dependencies**: Uses only Python standard library

### File Structure
```
organize_downloads.py           # Main script (300+ lines)
organize_config.example.json    # Example configuration
README.md                        # Complete documentation
USAGE_GUIDE.md                  # Quick reference guide
CHANGELOG.md                    # Version history
requirements.txt                # No external deps!
.kiro/project.json              # Project metadata
```

### Categories Supported
1. **Images** - jpg, png, gif, webp, bmp, svg, ico
2. **Documents** - pdf, docx, xlsx, txt, pptx, csv, odt
3. **Videos** - mp4, mkv, mov, avi, flv, wmv, webm
4. **Archives** - zip, rar, 7z, tar, gz, bz2, xz
5. **Installers** - exe, msi, dmg, deb, rpm, pkg, apk
6. **Music** - mp3, wav, flac, aac, ogg, m4a, wma
7. **Code** - py, js, java, cpp, c, cs, php, rb, go, ts, html, css

---

## Usage Examples

### Basic Organization
```bash
# Safe preview
python organize_downloads.py --dry-run

# Organize Downloads
python organize_downloads.py

# Organize with dates
python organize_downloads.py --by-date

# Undo last operation
python organize_downloads.py --undo
```

### Advanced Usage
```bash
# Custom folder
python organize_downloads.py --path "C:\MyFolder"

# Date-based with custom path
python organize_downloads.py --path "D:\Archive" --by-date

# Preview date-based organization
python organize_downloads.py --by-date --dry-run
```

---

## Why This Solution Stands Out

1. **Production-ready**: Not just a proof of concept
2. **User-friendly**: Dry-run mode prevents mistakes
3. **Extensible**: Easy to add new categories or features
4. **Well-documented**: README, usage guide, and changelog
5. **Safe**: Undo functionality and comprehensive error handling
6. **Zero setup**: No dependencies to install
7. **Cross-platform**: Works on Windows, macOS, and Linux

---

## Future Enhancement Ideas

1. **Scheduled automation** via cron/Task Scheduler
2. **GUI version** with drag-and-drop
3. **Duplicate file detection** and removal
4. **File size-based organization** (large files separate)
5. **Smart naming** based on content analysis
6. **Cloud integration** (Google Drive, Dropbox)

---

## Testing Checklist

✅ Dry-run mode works correctly  
✅ Files moved to correct categories  
✅ Duplicate filenames handled  
✅ System files skipped  
✅ Logging works properly  
✅ Date-based organization creates correct structure  
✅ Custom config loaded and applied  
✅ Undo restores files correctly  
✅ Error handling works gracefully  
✅ Cross-platform paths handled  

---

## Conclusion

This project demonstrates "lazy automation" by eliminating the tedious task of manually organizing downloads. The three polish improvements (date-based organization, configurable categories, and undo functionality) transform it from a simple script into a robust, production-ready tool that users can trust with their files.

**Time saved per use**: ~5-10 minutes  
**Lines of code**: ~350  
**External dependencies**: 0  
**Platforms supported**: 3 (Windows, macOS, Linux)  
**File types supported**: 50+  

---

**Made with ❤️ for AI for Bharat – Kiro Week 2 Challenge**
