# Quick Start

## For Lazy People

Don't read the README. Just do this:

### Option 1: Terminal (Fastest)
```bash
cd macos-folder-organizer
python3 skill/scripts/organize_folder.py ~/Downloads
```

Done. Your Downloads is organized.

### Option 2: Cowork (Even Easier)
1. Download the `find-duplicates.skill` file from this repo
2. In Cowork, click "Add Skill" → select the file
3. Tell Claude: "Organize my Downloads"
4. Done.

That's it. Seriously.

## What Happens

Your folder transforms from chaos to organized:

```
Before:
[Downloads]
  - 45634_final_v2.png
  - random_image_23.jpg
  - document_final_copy_v3.pdf
  - ... (1,310 more files)

After:
[Downloads]
  ├── Logos/ (smart-named files)
  ├── Documents/
  ├── Videos/
  ├── Design_Files/
  └── 8 more organized folders
```

## Installation

### No Installation (Just Run It)
```bash
python3 skill/scripts/organize_folder.py /path/to/folder
```

### With Cowork
Download `find-duplicates.skill` → Add to Cowork → Done

That's literally everything you need to know.
