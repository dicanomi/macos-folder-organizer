# macOS Folder Organizer

One-shot folder organization for lazy people with high IQs. Point it at any folder and it organizes everything instantly: renames chaotic files, sorts them into logical categories, and moves duplicates aside.

No confirmations. No dry runs. Just done.

## What It Does

### Smart Renaming
Transforms chaos into clarity:
- `45634_final_v2.png` → `logo_freepik_grey.svg`
- `random_image_23.jpg` → `background_texture.jpg`
- `137615683_d620242d.psd` → `illustration_design_mockup.psd`

The script analyzes filenames and file types, extracting meaningful words and organizing them into readable names.

### Automatic Categorization
Sorts files into 12 logical folders:
- **Logos** - brand marks, symbols, icons
- **Backgrounds** - wallpapers, textures, backdrops
- **Illustrations** - artwork, designs, graphics
- **Product_Images** - mockups, renders, product photos
- **Screenshots** - screen captures
- **Icons** - small icon files
- **Documents** - PDFs, Word docs, spreadsheets
- **Videos** - MP4, MOV, WebM, etc.
- **Archives** - ZIP, RAR, 7Z files
- **Design_Files** - PSD, AI, Sketch, InDesign
- **Code** - Python, JavaScript, HTML, CSS
- **Audio** - MP3, WAV, FLAC
- **Other** - everything else

### Duplicate Detection
Finds files with the same name in different locations and moves them to a dated `_Duplicates_[DATE]/` folder so you can review and delete later.

## Installation

### For Cowork Users (Recommended)
1. Download the `.skill` file from this repo
2. In Cowork, click "Add Skill" and select the downloaded file
3. Done

### For Terminal Users
```bash
# Clone the repo
git clone https://github.com/dicanomi/macos-folder-organizer.git
cd macos-folder-organizer

# Run the organizer
python3 scripts/organize_folder.py ~/Downloads
python3 scripts/organize_folder.py ~/Desktop
python3 scripts/organize_folder.py /path/to/any/folder
```

## Usage

### In Cowork
Just tell Claude:
```
"Organize my Downloads"
"Clean up my Desktop"
"Organize ~/Google Drive/Projects"
```

That's it. Claude runs the organizer and your folder is organized.

### From Terminal
```bash
python3 organize_folder.py <folder_path>
```

Example:
```bash
python3 organize_folder.py ~/Downloads
```

## Before & After

### Downloads Folder Example
**Before:** 1,313 chaotic files mixed together

```
[Downloads]
  - 45634_final_v2.png
  - random_image_23.jpg
  - 137615683_d620242d.psd
  - document_final_copy_v3.pdf
  - archive_2025_backup.zip
  - screenshot_01.png
  - ... (1,307 more files)
```

**After:** Organized into 12 categories with readable names

```
[Downloads]
  ├── Logos/ (247 files)
  │   ├── logo_freepik_grey.svg
  │   ├── logo_alchemy_brandidentity.indd
  │   └── ...
  ├── Illustrations/ (191 files)
  │   ├── illustration_design_mockup.psd
  │   └── ...
  ├── Design_Files/ (139 files)
  ├── Documents/ (124 files)
  ├── Archives/ (128 files)
  ├── Videos/ (93 files)
  ├── Backgrounds/ (105 files)
  ├── Screenshots/ (83 files)
  ├── Product_Images/ (55 files)
  ├── Icons/ (37 files)
  ├── Code/ (14 files)
  └── Other/ (97 files)
```

### Desktop Example
**Before:** 74 random files

```
[Desktop]
  - Screenshot 2025-05-13 at 3.45.12 PM.png
  - design_mockup_final.psd
  - report.pdf
  - video_clip.mp4
  - ... (70 more files)
```

**After:** Clean and organized

```
[Desktop]
  ├── Screenshots/ (32 files)
  ├── Illustrations/ (15 files)
  ├── Other/ (10 files)
  ├── Backgrounds/ (7 files)
  ├── Product_Images/ (6 files)
  ├── Documents/ (2 files)
  └── Logos/ (2 files)
```

## Features

✅ **One-shot execution** - No confirmations, no dry runs, just organize  
✅ **Smart naming** - Extracts meaningful words from filenames  
✅ **Intelligent categorization** - Uses file extensions and content analysis  
✅ **Duplicate detection** - Moves duplicate files to a dated folder  
✅ **No subdirectories** - Only organizes root-level files (keeps project folders intact)  
✅ **Safe** - Creates category folders automatically  
✅ **Fast** - Processes 1,000+ files in seconds  

## For Lazy Users

You don't need to understand anything about this. Just use it:

```bash
python3 organize_folder.py ~/Downloads
```

Or in Cowork:
```
Claude, organize my Downloads
```

That's genuinely it. Your folder is organized. Go do something more important.

## Technical Details

### What Gets Organized
- Root-level files only (doesn't touch your project folders)
- Skips hidden files (starting with `.`)
- Skips system files (`.DS_Store`, `Thumbs.db`)
- Skips the script itself (`.py` files)

### Smart Naming Algorithm
1. Analyzes filename for keywords (logo, background, screenshot, etc.)
2. Looks at file extension to infer type
3. For images, analyzes dimensions (small = icon, large = background)
4. Extracts meaningful words from the original filename
5. Generates readable new name: `[prefix]_[descriptor].[ext]`

Example: `freepik__a-grey-textured-minimal-design-based-on-the-reference_45634_final_v2.png`
→ Extract: `freepik`, `grey`, `textured`
→ Result: `logo_freepik_grey.svg`

### Duplicate Detection
Finds files with identical names (case-insensitive) across the folder and moves them to `_Duplicates_[DATE_TIME]/` for manual review.

## Requirements

- macOS (works on any OS with Python 3.7+)
- Python 3.7+
- Pillow (optional, for image dimension analysis): `pip install Pillow`

## License

MIT License - free to use, modify, and distribute

## Contributing

Found a bug? Have a suggestion? Open an issue or submit a PR.

## Author

Created by [dicanomi](https://github.com/dicanomi)

## Questions?

Just organize a folder and see what it does. It's faster than reading docs.
