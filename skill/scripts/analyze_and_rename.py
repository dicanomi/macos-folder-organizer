#!/usr/bin/env python3
"""
Analyze file content and rename intelligently based on what they actually are
Identifies logos, images, backgrounds, documents, and more
Optimized for speed - samples large directories
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import random

try:
    from PIL import Image
except ImportError:
    Image = None

CONTENT_PATTERNS = {
    'Logos': {
        'extensions': ['.png', '.svg', '.ai', '.eps'],
        'keywords': ['logo', 'mark', 'icon', 'symbol', 'brand'],
    },
    'Backgrounds': {
        'extensions': ['.png', '.jpg', '.jpeg'],
        'keywords': ['background', 'bg', 'wallpaper', 'backdrop', 'texture'],
    },
    'Product_Images': {
        'extensions': ['.png', '.jpg', '.jpeg'],
        'keywords': ['product', 'item', 'photo', 'render', 'mockup'],
    },
    'Screenshots': {
        'extensions': ['.png', '.jpg', '.jpeg'],
        'keywords': ['screenshot', 'screen', 'capture', 'snap'],
    },
    'Illustrations': {
        'extensions': ['.png', '.jpg', '.jpeg', '.psd', '.ai'],
        'keywords': ['illustration', 'draw', 'art', 'design', 'graphic'],
    },
    'Icons': {
        'extensions': ['.png', '.svg', '.ico'],
        'keywords': ['icon', 'glyph', 'symbol'],
    },
    'Documents': {
        'extensions': ['.pdf', '.doc', '.docx', '.xlsx', '.pptx', '.rtf', '.txt'],
        'keywords': [],
    },
    'Videos': {
        'extensions': ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.wmv', '.m4v'],
        'keywords': [],
    },
    'Archives': {
        'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
        'keywords': [],
    },
    'Design_Files': {
        'extensions': ['.psd', '.ai', '.sketch', '.figma', '.xd', '.indd', '.eps'],
        'keywords': [],
    }
}

def get_image_dimensions(filepath):
    """Get image width/height in pixels"""
    if not Image:
        return None
    try:
        with Image.open(filepath) as img:
            return img.size
    except:
        return None

def analyze_file(filepath):
    """
    Analyze file and determine category and suggested name
    Returns: (category, suggested_name_prefix)
    """
    filename = os.path.basename(filepath)
    ext = Path(filename).suffix.lower()
    filename_lower = filename.lower()

    # Check for matching extension/keywords
    for category, patterns in CONTENT_PATTERNS.items():
        if ext in patterns['extensions']:
            for keyword in patterns['keywords']:
                if keyword in filename_lower:
                    return (category, keyword)
            return (category, 'file')

    # Image heuristics
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        # Check filename keywords
        for keyword in ['logo', 'icon', 'background', 'bg']:
            if keyword in filename_lower:
                if keyword in ['logo', 'icon']:
                    return ('Logos', keyword)
                else:
                    return ('Backgrounds', keyword)

        # Try dimensions
        if Image:
            dims = get_image_dimensions(filepath)
            if dims:
                width, height = dims
                max_dim = max(width, height)

                if max_dim < 500:
                    return ('Icons', 'icon')
                elif max_dim > 2000:
                    return ('Backgrounds', 'background')

        return ('Illustrations', 'image')

    return ('Other', 'file')

def generate_name(base_prefix, original_filename, category):
    """Generate a friendly name"""
    original = Path(original_filename).stem
    original = original.replace('_', ' ').replace('-', ' ')

    junk_patterns = ['final', 'v1', 'v2', 'v3', 'copy', 'backup', 'old', 'new',
                     'test', 'temp', 'tmp', 'unused', 'archive', 'draft', 'design',
                     'file', 'image', 'photo', 'pic', 'img', 'document']

    words = [w for w in original.split() if w.lower() not in junk_patterns and len(w) > 2]

    if words and len(words) > 0:
        descriptor = ' '.join(words[:2]).lower().replace(' ', '_')
        suggested_name = f"{base_prefix}_{descriptor}"
    else:
        suggested_name = base_prefix

    return suggested_name[:50]  # Cap length

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_and_rename.py <folder_path>")
        sys.exit(1)

    folder_path = os.path.expanduser(sys.argv[1])

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} not found")
        sys.exit(1)

    # Collect root-level files only (not recursive)
    files_to_process = []
    skip_extensions = {'.py', '.pyc', '.json', '.txt', '.csv', '.xlsx', '.rtf'}
    skip_names = {'.DS_Store', '.gitignore'}

    print(f"Scanning {folder_path}...\n")

    items = os.listdir(folder_path)
    files_in_root = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

    print(f"Found {len(files_in_root)} files in root")

    for item in files_in_root:
        if item.startswith('.') or item in skip_names:
            continue
        filepath = os.path.join(folder_path, item)
        if Path(item).suffix.lower() not in skip_extensions:
            files_to_process.append((filepath, item))

    if not files_to_process:
        print("No files to process!")
        return

    print(f"Processing {len(files_to_process)} files\n")
    print("="*80)
    print("FILE ANALYSIS AND PROPOSED ORGANIZATION")
    print("="*80 + "\n")

    by_category = defaultdict(list)
    for filepath, filename in files_to_process:
        category, prefix = analyze_file(filepath)
        new_name = generate_name(prefix, filename, category)
        ext = Path(filename).suffix.lower()

        by_category[category].append({
            'original': filename,
            'new': f"{new_name}{ext}",
            'path': filepath
        })

    # Show summary
    for category in sorted(by_category.keys()):
        files = by_category[category]
        print(f"\n{category}: {len(files)} files")
        for item in files[:3]:
            orig = item['original']
            if len(orig) > 60:
                orig = orig[:57] + "..."
            new = item['new']
            if len(new) > 60:
                new = new[:57] + "..."
            print(f"  {orig}")
            print(f"  -> {new}\n")
        if len(files) > 3:
            print(f"  ... and {len(files) - 3} more\n")

    print("="*80)
    print("\nFolders that would be created:")
    for category in sorted(by_category.keys()):
        print(f"  - {category}/")
    print("\n" + "="*80)
    print("\nThis is a DRY RUN (no changes made).")
    print("To apply these changes, use the find-duplicates skill and select 'apply'.")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
