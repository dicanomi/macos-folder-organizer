#!/usr/bin/env python3
"""
One-shot folder organizer: categorize files, rename intelligently, move duplicates
No confirmations. No dry runs. Just organize root-level files.
"""

import os
import sys
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    Image = None

CATEGORIES = {
    'Logos': ['.png', '.svg', '.ai', '.eps'],
    'Backgrounds': ['.png', '.jpg', '.jpeg'],
    'Illustrations': ['.psd', '.png', '.jpg', '.jpeg', '.ai'],
    'Product_Images': ['.png', '.jpg', '.jpeg'],
    'Screenshots': ['.png', '.jpg', '.jpeg'],
    'Icons': ['.png', '.svg', '.ico'],
    'Documents': ['.pdf', '.doc', '.docx', '.xlsx', '.pptx', '.rtf', '.txt'],
    'Videos': ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.wmv', '.m4v'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
    'Design_Files': ['.psd', '.ai', '.sketch', '.figma', '.xd', '.indd', '.eps'],
    'Code': ['.py', '.js', '.jsx', '.tsx', '.ts', '.html', '.css', '.json'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg'],
    'Other': []
}

def analyze_file(filepath):
    """Determine file category and suggested name based on extension and keywords"""
    filename = os.path.basename(filepath)
    ext = Path(filename).suffix.lower()
    filename_lower = filename.lower()

    # Keywords for intelligent naming
    logo_keywords = ['logo', 'mark', 'brand', 'symbol', 'icon']
    bg_keywords = ['background', 'bg', 'wallpaper', 'backdrop', 'texture']
    product_keywords = ['product', 'mockup', 'render', 'hero']
    screenshot_keywords = ['screenshot', 'screen', 'capture', 'snap']
    illustration_keywords = ['illustration', 'art', 'graphic', 'draw']

    # Check keywords first
    for keyword in logo_keywords:
        if keyword in filename_lower:
            return ('Logos', 'logo')

    for keyword in bg_keywords:
        if keyword in filename_lower:
            return ('Backgrounds', 'background')

    for keyword in product_keywords:
        if keyword in filename_lower:
            return ('Product_Images', 'product')

    for keyword in screenshot_keywords:
        if keyword in filename_lower:
            return ('Screenshots', 'screenshot')

    for keyword in illustration_keywords:
        if keyword in filename_lower:
            return ('Illustrations', 'illustration')

    # Extension-based categorization
    for category, extensions in CATEGORIES.items():
        if category == 'Other':
            continue
        if ext in extensions:
            if ext == '.png':
                if Image:
                    try:
                        with Image.open(filepath) as img:
                            w, h = img.size
                            if w < 500 and h < 500:
                                return ('Icons', 'icon')
                            elif w > 2000 or h > 2000:
                                return ('Backgrounds', 'background')
                    except:
                        pass
                return ('Illustrations', 'image')
            elif ext in ['.jpg', '.jpeg']:
                return ('Illustrations', 'image')
            elif ext == '.ai':
                return ('Design_Files', 'vector')
            elif ext == '.psd':
                return ('Design_Files', 'design')
            else:
                return (category, category.lower())

    return ('Other', 'file')

def generate_filename(original, category, prefix):
    """Generate readable filename from original"""
    stem = Path(original).stem
    ext = Path(original).suffix.lower()

    junk = ['final', 'v1', 'v2', 'v3', 'copy', 'backup', 'old', 'new',
            'test', 'temp', 'draft', 'archive', 'file', 'image', 'photo', 'design', 'doc']

    words = [w for w in stem.replace('_', ' ').replace('-', ' ').split()
             if w.lower() not in junk and len(w) > 2]

    if words:
        desc = '_'.join(words[:2]).lower()[:30]
        new_name = f"{prefix}_{desc}"
    else:
        new_name = prefix

    return f"{new_name}{ext}"

def organize_folder(folder_path):
    """Organize folder: categorize and rename root-level files only"""
    folder_path = os.path.expanduser(folder_path)

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} not found")
        return

    print(f"\nOrganizing: {folder_path}")
    print("="*70)

    # Create category folders
    for category in CATEGORIES.keys():
        cat_path = os.path.join(folder_path, category)
        os.makedirs(cat_path, exist_ok=True)

    # Create dated duplicates folder
    date_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    duplicates_folder = os.path.join(folder_path, f'_Duplicates_{date_str}')
    os.makedirs(duplicates_folder, exist_ok=True)

    # Scan ROOT-LEVEL FILES ONLY
    files_by_name = defaultdict(list)
    all_files = []
    skip_items = {'.DS_Store', '.gitignore', 'Thumbs.db', '.AppleDouble'}
    skip_ext = {'.py', '.pyc'}

    print("Scanning root-level files...")
    for item in os.listdir(folder_path):
        if item.startswith('.') or item.startswith('_Duplicates_') or item.startswith('_'):
            continue
        if item in skip_items:
            continue

        filepath = os.path.join(folder_path, item)

        # Skip directories
        if os.path.isdir(filepath):
            continue

        if Path(item).suffix.lower() in skip_ext:
            continue

        all_files.append((filepath, item))

        # Track by name (case-insensitive) for duplicate detection
        name_key = Path(item).name.lower()
        files_by_name[name_key].append(filepath)

    print(f"Found {len(all_files)} files")

    # Identify simple duplicates (same filename)
    duplicates = set()
    for paths in files_by_name.values():
        if len(paths) > 1:
            duplicates.update(paths)

    print(f"Found {len(duplicates)} duplicates")

    # Organize files
    moved = 0
    by_category = defaultdict(int)

    for filepath, filename in sorted(all_files):
        category, prefix = analyze_file(filepath)
        new_filename = generate_filename(filename, category, prefix)

        # Determine destination
        if filepath in duplicates:
            dest_folder = duplicates_folder
            display_cat = 'Duplicates'
        else:
            dest_folder = os.path.join(folder_path, category)
            display_cat = category

        dest_path = os.path.join(dest_folder, new_filename)

        # Handle naming conflicts
        if os.path.exists(dest_path) and dest_path != filepath:
            base, ext = os.path.splitext(new_filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

        try:
            if os.path.dirname(filepath) != os.path.dirname(dest_path) or new_filename != filename:
                shutil.move(filepath, dest_path)
                moved += 1
                by_category[display_cat] += 1
        except Exception as e:
            print(f"Error: {filename} - {e}")

    # Clean up empty category folders
    for category in CATEGORIES.keys():
        cat_path = os.path.join(folder_path, category)
        try:
            if os.path.isdir(cat_path) and len(os.listdir(cat_path)) == 0:
                os.rmdir(cat_path)
        except:
            pass

    # Clean up empty duplicates folder
    try:
        if len(os.listdir(duplicates_folder)) == 0:
            os.rmdir(duplicates_folder)
    except:
        pass

    # Report
    print("\n" + "="*70)
    print(f"✓ Organized {moved} files")

    for cat in sorted(by_category.keys()):
        count = by_category[cat]
        print(f"  {cat}: {count} files")

    print("="*70 + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: organize_folder.py <folder_path>")
        sys.exit(1)

    organize_folder(sys.argv[1])
