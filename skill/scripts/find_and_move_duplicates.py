#!/usr/bin/env python3
"""
Find and move duplicate files into dated Duplicates folder with categorized subfolders
Supports filename matching, content hashing, or both
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.eps'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg', '.aiff'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.pages', '.numbers', '.keynote'],
    'Design Files': ['.psd', '.ai', '.sketch', '.figma', '.xd', '.indd'],
    'Code': ['.py', '.js', '.html', '.css', '.json', '.xml', '.java', '.cpp', '.swift', '.ts', '.tsx', '.jsx'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
    'Other': []
}

def get_file_hash(filepath):
    """Get SHA256 hash of file (first 100KB for speed)"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            data = f.read(102400)
            sha256.update(data)
        return sha256.hexdigest()
    except:
        return None

def get_category(filename):
    """Get category based on file extension"""
    ext = Path(filename).suffix.lower()
    for category, extensions in CATEGORIES.items():
        if category == 'Other':
            continue
        if ext in extensions:
            return category
    return 'Other'

def format_size(size_bytes):
    """Convert bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def find_duplicates(folder_path, detection_mode='both'):
    """
    Find duplicate files
    detection_mode: 'filename', 'content', or 'both'
    Returns: duplicates set, total_files count, statistics dict
    """
    all_files = []
    skip_extensions = {'.py', '.txt', '.xlsx'}

    print(f"Scanning {folder_path}...\n")

    # Scan files
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('Duplicates-')]

        for filename in files:
            if filename.startswith('.') or Path(filename).suffix.lower() in skip_extensions:
                continue
            filepath = os.path.join(root, filename)
            all_files.append((filepath, filename))

    print(f"Found {len(all_files)} total files\n")

    stats = {
        'total_files': len(all_files),
        'filename_duplicates': 0,
        'content_duplicates': 0,
        'total_duplicates': 0,
        'wasted_space_bytes': 0
    }

    duplicates = set()

    # Filename matching
    if detection_mode in ('filename', 'both'):
        print("Finding filename duplicates...")
        filenames_dict = defaultdict(list)
        for filepath, filename in all_files:
            filenames_dict[filename.lower()].append((filepath, filename))

        for fname, paths in filenames_dict.items():
            if len(paths) > 1:
                for filepath, _ in paths:
                    duplicates.add(filepath)
                    stats['filename_duplicates'] += 1

        print(f"  Found {stats['filename_duplicates']} filename duplicates\n")

    # Content hashing
    if detection_mode in ('content', 'both'):
        print("Finding content duplicates...")
        remaining_files = [(p, f) for p, f in all_files if p not in duplicates]

        hashes_dict = defaultdict(list)
        for i, (filepath, filename) in enumerate(remaining_files):
            if i % 500 == 0 and i > 0:
                print(f"  Hashed {i}/{len(remaining_files)}...")
            fhash = get_file_hash(filepath)
            if fhash:
                try:
                    size = os.path.getsize(filepath)
                    hashes_dict[fhash].append({'path': filepath, 'size': size})
                except:
                    pass

        for fhash, file_list in hashes_dict.items():
            if len(file_list) > 1:
                for item in file_list[1:]:  # All but first (keep the first)
                    duplicates.add(item['path'])
                    stats['content_duplicates'] += 1
                    stats['wasted_space_bytes'] += item['size']

        print(f"  Found {stats['content_duplicates']} content duplicates\n")

    # Calculate total wasted space
    for filepath in duplicates:
        try:
            stats['wasted_space_bytes'] += os.path.getsize(filepath)
        except:
            pass

    stats['total_duplicates'] = len(duplicates)
    return duplicates, stats

def dry_run(folder_path, duplicates, stats):
    """Show what would be moved without actually moving"""
    print("="*70)
    print("DRY RUN: What would be moved")
    print("="*70)
    print(f"Total files scanned: {stats['total_files']}")
    print(f"Filename duplicates: {stats['filename_duplicates']}")
    print(f"Content duplicates: {stats['content_duplicates']}")
    print(f"TOTAL duplicates to move: {stats['total_duplicates']}")
    print(f"Space to free: {format_size(stats['wasted_space_bytes'])}")
    print("="*70)

    by_category = defaultdict(int)
    for filepath in duplicates:
        filename = os.path.basename(filepath)
        category = get_category(filename)
        by_category[category] += 1

    print("\nFiles by category:\n")
    for category in sorted(by_category.keys()):
        print(f"  {category}: {by_category[category]} files")

    print("\n" + "="*70)
    return by_category

def move_duplicates(folder_path, duplicates):
    """Actually move the files"""
    # Create dated duplicates folder
    date_str = datetime.now().strftime('%Y-%m-%d')
    duplicates_folder = os.path.join(folder_path, f'Duplicates-{date_str}')

    # Create category subfolders
    for category in CATEGORIES.keys():
        os.makedirs(os.path.join(duplicates_folder, category), exist_ok=True)

    moved = 0
    errors = []
    by_category = defaultdict(int)
    total_wasted = 0

    print(f"\nMoving files to {duplicates_folder}...\n")

    for i, filepath in enumerate(sorted(duplicates)):
        if not os.path.exists(filepath):
            continue

        filename = os.path.basename(filepath)
        category = get_category(filename)
        dest_folder = os.path.join(duplicates_folder, category)
        dest_path = os.path.join(dest_folder, filename)

        # Handle naming conflicts
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

        try:
            shutil.move(filepath, dest_path)
            moved += 1
            by_category[category] += 1
            try:
                total_wasted += os.path.getsize(dest_path)
            except:
                pass
            if moved % 100 == 0:
                print(f"✓ Moved {moved} files...")
        except Exception as e:
            errors.append((filename, str(e)))

    # Generate JSON report
    report = {
        'timestamp': datetime.now().isoformat(),
        'folder': folder_path,
        'duplicates_folder': duplicates_folder,
        'total_files_scanned': len(duplicates),
        'files_moved': moved,
        'space_freed_bytes': total_wasted,
        'space_freed': format_size(total_wasted),
        'by_category': dict(by_category),
        'errors': len(errors)
    }

    report_path = os.path.join(duplicates_folder, 'duplicate_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    # Summary
    print("\n" + "="*70)
    print(f"SUCCESS: Moved {moved} files to {duplicates_folder}/")
    print("="*70)
    for category in sorted(by_category.keys()):
        print(f"  {category}: {by_category[category]} files")
    print(f"\nSpace freed: {format_size(total_wasted)}")
    if errors:
        print(f"Errors: {len(errors)}")
    print(f"\nReport: {report_path}")
    print("="*70 + "\n")

    return duplicates_folder

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: find_and_move_duplicates.py <folder_path> [detection_mode] [auto_move]")
        print("  detection_mode: 'filename', 'content', or 'both' (default: both)")
        print("  auto_move: 'yes' to skip confirmation (default: ask)")
        sys.exit(1)

    folder_path = os.path.expanduser(sys.argv[1])
    detection_mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
    auto_move = sys.argv[3] == 'yes' if len(sys.argv) > 3 else False

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} not found")
        sys.exit(1)

    # Find duplicates
    duplicates, stats = find_duplicates(folder_path, detection_mode)

    if not duplicates:
        print("No duplicates found!")
        return

    # Dry run
    dry_run(folder_path, duplicates, stats)

    # Ask before moving
    if not auto_move:
        response = input("\nProceed with moving these files? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return

    # Move files
    move_duplicates(folder_path, duplicates)

if __name__ == '__main__':
    main()
