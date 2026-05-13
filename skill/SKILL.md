---
name: find-duplicates
description: One-shot folder organization skill. Organize ANY folder by automatically categorizing files (Logos, Images, Documents, Videos, Design Files, Archives, etc.), intelligently renaming them based on content, and creating a dated Duplicates folder for files that appear multiple times. Just tell Claude the folder path and it handles everything - no confirmation needed, just pure organization. Works on Downloads, Google Drive folders, design libraries, project folders, anywhere. High IQ lazy user solution.
compatibility: Python 3.7+, filesystem access, hashlib
---

# One-Shot Folder Organizer

Point it at ANY folder and it organizes everything instantly:
- Renames chaotic filenames to be human-readable (e.g., "45634_final_v2.png" becomes "logo_freepik_grey.svg")
- Sorts files into 12 logical category folders:
  - Logos, Backgrounds, Illustrations, Product_Images, Screenshots, Icons
  - Documents, Videos, Archives, Design_Files, Code, Audio, Other
- Detects and moves duplicate files into a dated duplicates folder
- One command, no confirmations, no dry runs. Just done.

Perfect for lazy high-IQ users who want messy Downloads, Google Drive, or project folders fixed instantly.

## How it works

**Mode 1: Find and organize duplicates**
1. **Scan**: Walks the entire folder tree and catalogs every file
2. **Detect duplicates by filename**: If the same filename appears multiple times, they're marked as duplicates
3. **Detect duplicates by content**: Files with identical content (SHA256 hash) are marked as duplicates
4. **Dry run** (default): Shows you exactly what would be moved before doing it
5. **Move and categorize**: Moves all duplicates into `Duplicates-[DATE]/` with subfolders by type
6. **Report**: Generates a JSON summary of what was moved and space freed

**Mode 2: Intelligently rename and organize files**
1. **Scan**: Catalogs all files in the folder
2. **Analyze content**: Examines each file to determine what it actually is (logo, background image, product photo, document, etc.)
3. **Smart naming**: Renames files based on content (e.g., "45634_final_v2.png" becomes "logo_blue_gradient.png")
4. **Categorization**: Organizes files into logical folders (Logos, Images, Backgrounds, Documents, Design Files, Videos, etc.)
5. **Dry run**: Shows proposed changes before applying them
6. **Apply**: Renames and moves files into organized structure

## What you need to do

**For finding duplicates:**
Tell Claude:
- The folder path you want to scan
- Detection mode: filename-only, content-only, or both (default: both)
- Whether to do a dry run first or move immediately (default: dry run first, then ask)

**For smart renaming and organizing:**
Tell Claude:
- The folder you want to organize (e.g., Downloads)
- File types to focus on (or "all" to rename everything)
- Whether you want a dry run first (recommended: yes)

Claude handles the rest: analyzing, renaming, categorizing, organizing, and reporting.

## Example usage

**Organize Downloads (smart rename + organize):**
"Organize my Downloads folder with smart names and folders."
Result: 1,300+ chaotic files become 8 organized folders (Logos, Backgrounds, Documents, Videos, etc.) with readable names like "logo_blue_gradient.png" instead of "45634_final_v2.png"

**Find duplicates:**
"Clean up duplicates in my Dropbox folder. Show me what would happen first."
Result: Scans folder, detects 427 duplicate files, shows dry run report, asks before moving to `Duplicates-2026-05-13/`

**Fast filename-only duplicate detection:**
"Find duplicates in ~/Downloads but only by filename matching."
Result: Detects only exact filename matches (skips slower content hashing), runs dry run, shows report

## Dry run output

The dry run report shows:
- Total files scanned
- Duplicates found by filename
- Duplicates found by content
- Total duplicate files to be moved
- Space that would be freed
- How many files per category (Images, Videos, Documents, etc.)

You review this and decide whether to proceed.

## After files are moved

All duplicates live in a folder named `Duplicates-[DATE]` in your original folder. Inside:
- `Images/` — all duplicate image files
- `Videos/` — all duplicate video files
- `Documents/` — all duplicate PDFs, Word docs, spreadsheets, etc.
- `Design Files/` — all duplicate design files (.psd, .ai, etc.)
- `Code/` — all duplicate code files
- `Archives/` — all duplicate zip/rar/tar files
- `Other/` — anything that doesn't fit the above
- `duplicate_report.json` — detailed report with every duplicate group, file sizes, and which files are safe to delete

The date folder lets you keep multiple duplicate scans over time and decide later which ones to permanently delete.

## Things to know

- **Naming conflicts**: If a file already exists in the destination category folder, Claude automatically renames it (`filename_1.ext`, `filename_2.ext`, etc.)
- **What's skipped**: Python scripts (.py), text reports (.txt), and inventory files (.xlsx) are never moved (they're utilities)
- **Hidden files and system folders**: Automatically skipped (folders starting with `.`)
- **Speed**: Filename matching is fast. Content hashing (SHA256) takes longer with large files, but only runs on files not already flagged by filename matching
- **Safe**: You always get a dry run first. No files move without explicit approval.

## Picking detection mode

**Filename + Content (default)**: Catches everything. Slower with many files, but finds duplicates you might miss (same file with different names). Recommended for any serious cleanup.

**Filename only**: Fastest. Only finds files with identical names in different locations. Good for quick scans of organized folders.

**Content only**: Medium speed. Finds identical files regardless of name. Good if you suspect duplicates with different names (e.g., "photo.jpg" and "photo_backup.jpg").

---

**After the skill completes**, you'll have a `Duplicates-[DATE]/` folder ready to review. Open it in Finder, browse the subfolders, and delete anything you don't need. The JSON report tells you safe deletion recommendations.
