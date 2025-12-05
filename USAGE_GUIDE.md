# Quick Usage Guide

## First Time Setup

1. **Test it safely first:**
   ```bash
   python organize_downloads.py --dry-run
   ```
   This shows what would happen without moving any files.

2. **Run the organization:**
   ```bash
   python organize_downloads.py
   ```

3. **Check the results:**
   - Look in your Downloads folder for new category folders
   - Check `organize.log` for details

## Common Use Cases

### Organize with Date Folders
Perfect for keeping files organized by when you downloaded them:
```bash
python organize_downloads.py --by-date
```

Result structure:
```
Downloads/
├── Documents/
│   ├── 2025/
│   │   ├── December/
│   │   │   └── report.pdf
│   │   └── November/
│   │       └── invoice.pdf
```

### Custom Categories
Want to add your own categories or change existing ones?

1. Copy the example config to your Downloads folder:
   ```bash
   copy organize_config.example.json %USERPROFILE%\Downloads\organize_config.json
   ```

2. Edit `organize_config.json` in your Downloads folder:
   ```json
   {
     "categories": {
       "Work": [".docx", ".xlsx", ".pptx"],
       "Personal": [".jpg", ".png", ".mp4"],
       "Ebooks": [".epub", ".mobi", ".pdf"]
     }
   }
   ```

3. Run the script - it automatically uses your config!

### Undo a Mistake
Organized the wrong folder? No problem:
```bash
python organize_downloads.py --undo
```

This moves all files back to their original locations.

### Organize a Different Folder
```bash
python organize_downloads.py --path "C:\Users\YourName\Desktop"
```

## Tips & Tricks

1. **Always dry-run first** when trying new options
2. **Check the log file** if something unexpected happens
3. **The undo feature** keeps history of last 100 operations
4. **Config files** are loaded from the target folder, not the script location
5. **Hidden files** are automatically skipped for safety

## Troubleshooting

**"Permission denied" error:**
- Make sure you have write access to the folder
- Close any programs that might have files open

**Files not being categorized:**
- Check if the extension is in the categories list
- Add it to your custom config if needed

**Undo not working:**
- Undo only works if files haven't been moved/deleted manually
- Check `.organize_history.json` exists in the folder

## Automation Ideas

### Windows Task Scheduler
Run automatically every day:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 11 PM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\organize_downloads.py`

### Linux/macOS Cron
Add to crontab:
```bash
# Run every day at 11 PM
0 23 * * * /usr/bin/python3 /path/to/organize_downloads.py
```
