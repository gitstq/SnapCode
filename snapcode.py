#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapCode - Lightweight Code Snapshot Management Tool
A zero-dependency CLI tool for managing code snapshots with diff, restore, and export capabilities.

Author: SnapCode Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import difflib

# Version
VERSION = "1.0.0"

# Default snapshot directory
DEFAULT_SNAP_DIR = ".snapcode"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.END}"
    return text

def print_success(msg: str):
    """Print success message."""
    print(f"{colorize('✓', Colors.GREEN)} {msg}")

def print_error(msg: str):
    """Print error message."""
    print(f"{colorize('✗', Colors.RED)} {msg}", file=sys.stderr)

def print_info(msg: str):
    """Print info message."""
    print(f"{colorize('ℹ', Colors.CYAN)} {msg}")

def print_warning(msg: str):
    """Print warning message."""
    print(f"{colorize('⚠', Colors.YELLOW)} {msg}")

def calculate_file_hash(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""

def get_file_info(filepath: str) -> Dict:
    """Get file information including hash and metadata."""
    try:
        stat = os.stat(filepath)
        return {
            "path": filepath,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "hash": calculate_file_hash(filepath)
        }
    except Exception as e:
        return {"path": filepath, "error": str(e)}

def load_config(snap_dir: str) -> Dict:
    """Load configuration from snapshot directory."""
    config_path = os.path.join(snap_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": VERSION,
        "created": datetime.now().isoformat(),
        "snapshots": [],
        "ignore_patterns": [
            "*.pyc", "__pycache__", ".git", ".snapcode",
            "node_modules", "*.log", ".env", "*.swp",
            ".DS_Store", "Thumbs.db", "*.tmp"
        ]
    }

def save_config(snap_dir: str, config: Dict):
    """Save configuration to snapshot directory."""
    config_path = os.path.join(snap_dir, "config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def should_ignore(path: str, ignore_patterns: List[str]) -> bool:
    """Check if path should be ignored based on patterns."""
    import fnmatch
    name = os.path.basename(path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path, pattern):
            return True
    return False

def collect_files(directory: str, ignore_patterns: List[str]) -> List[str]:
    """Collect all files in directory recursively."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # Filter directories
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if not should_ignore(filepath, ignore_patterns):
                files.append(filepath)
    return files

def create_snapshot(directory: str, name: str, message: str = "") -> Dict:
    """Create a new code snapshot."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    
    # Create snapshot directory if not exists
    os.makedirs(snap_dir, exist_ok=True)
    
    # Load config
    config = load_config(snap_dir)
    
    # Generate snapshot ID
    snapshot_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    if name:
        snapshot_id = f"{snapshot_id}_{name}"
    
    # Check if snapshot with same name exists
    for snap in config["snapshots"]:
        if snap.get("name") == name and name:
            print_error(f"Snapshot with name '{name}' already exists")
            return None
    
    # Collect files
    files = collect_files(directory, config.get("ignore_patterns", []))
    
    if not files:
        print_warning("No files found to snapshot")
        return None
    
    # Create snapshot data directory
    snapshot_data_dir = os.path.join(snap_dir, "data", snapshot_id)
    os.makedirs(snapshot_data_dir, exist_ok=True)
    
    # Copy files and create manifest
    manifest = {
        "id": snapshot_id,
        "name": name,
        "message": message,
        "created": datetime.now().isoformat(),
        "files": []
    }
    
    total_size = 0
    for filepath in files:
        rel_path = os.path.relpath(filepath, directory)
        file_info = get_file_info(filepath)
        file_info["relative_path"] = rel_path
        manifest["files"].append(file_info)
        total_size += file_info.get("size", 0)
        
        # Copy file to snapshot directory
        dest_path = os.path.join(snapshot_data_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(filepath, dest_path)
    
    manifest["total_files"] = len(files)
    manifest["total_size"] = total_size
    
    # Save manifest
    manifest_path = os.path.join(snapshot_data_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    # Update config
    config["snapshots"].append({
        "id": snapshot_id,
        "name": name,
        "message": message,
        "created": manifest["created"],
        "files_count": len(files),
        "total_size": total_size
    })
    save_config(snap_dir, config)
    
    return manifest

def list_snapshots(directory: str) -> List[Dict]:
    """List all snapshots."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    config_path = os.path.join(snap_dir, "config.json")
    
    if not os.path.exists(config_path):
        return []
    
    config = load_config(snap_dir)
    return config.get("snapshots", [])

def get_snapshot_manifest(directory: str, snapshot_id: str) -> Optional[Dict]:
    """Get snapshot manifest by ID."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    manifest_path = os.path.join(snap_dir, "data", snapshot_id, "manifest.json")
    
    if not os.path.exists(manifest_path):
        return None
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def restore_snapshot(directory: str, snapshot_id: str, dry_run: bool = False) -> Dict:
    """Restore files from a snapshot."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    snapshot_data_dir = os.path.join(snap_dir, "data", snapshot_id)
    
    if not os.path.exists(snapshot_data_dir):
        print_error(f"Snapshot '{snapshot_id}' not found")
        return None
    
    manifest = get_snapshot_manifest(directory, snapshot_id)
    if not manifest:
        print_error("Failed to load snapshot manifest")
        return None
    
    result = {
        "restored": [],
        "skipped": [],
        "errors": []
    }
    
    for file_info in manifest.get("files", []):
        rel_path = file_info.get("relative_path")
        src_path = os.path.join(snapshot_data_dir, rel_path)
        dest_path = os.path.join(directory, rel_path)
        
        if not os.path.exists(src_path):
            result["errors"].append({"path": rel_path, "error": "Source file not found"})
            continue
        
        if dry_run:
            result["restored"].append(rel_path)
            continue
        
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            result["restored"].append(rel_path)
        except Exception as e:
            result["errors"].append({"path": rel_path, "error": str(e)})
    
    return result

def delete_snapshot(directory: str, snapshot_id: str) -> bool:
    """Delete a snapshot."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    snapshot_data_dir = os.path.join(snap_dir, "data", snapshot_id)
    
    if not os.path.exists(snapshot_data_dir):
        print_error(f"Snapshot '{snapshot_id}' not found")
        return False
    
    # Remove snapshot data
    shutil.rmtree(snapshot_data_dir)
    
    # Update config
    config = load_config(snap_dir)
    config["snapshots"] = [s for s in config["snapshots"] if s["id"] != snapshot_id]
    save_config(snap_dir, config)
    
    return True

def diff_snapshots(directory: str, snapshot_id1: str, snapshot_id2: str) -> Dict:
    """Compare two snapshots and show differences."""
    manifest1 = get_snapshot_manifest(directory, snapshot_id1)
    manifest2 = get_snapshot_manifest(directory, snapshot_id2)
    
    if not manifest1:
        print_error(f"Snapshot '{snapshot_id1}' not found")
        return None
    if not manifest2:
        print_error(f"Snapshot '{snapshot_id2}' not found")
        return None
    
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    
    # Build file maps
    files1 = {f["relative_path"]: f for f in manifest1.get("files", [])}
    files2 = {f["relative_path"]: f for f in manifest2.get("files", [])}
    
    all_paths = set(files1.keys()) | set(files2.keys())
    
    result = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": []
    }
    
    for path in sorted(all_paths):
        if path not in files1:
            result["added"].append(path)
        elif path not in files2:
            result["removed"].append(path)
        elif files1[path].get("hash") != files2[path].get("hash"):
            result["modified"].append(path)
        else:
            result["unchanged"].append(path)
    
    return result

def show_file_diff(directory: str, snapshot_id1: str, snapshot_id2: str, filepath: str) -> str:
    """Show detailed diff for a specific file."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    
    file1_path = os.path.join(snap_dir, "data", snapshot_id1, filepath)
    file2_path = os.path.join(snap_dir, "data", snapshot_id2, filepath)
    
    def read_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except Exception:
            return []
    
    lines1 = read_file(file1_path) if os.path.exists(file1_path) else []
    lines2 = read_file(file2_path) if os.path.exists(file2_path) else []
    
    diff = difflib.unified_diff(
        lines1, lines2,
        fromfile=f"{snapshot_id1}/{filepath}",
        tofile=f"{snapshot_id2}/{filepath}",
        lineterm=''
    )
    
    return ''.join(diff)

def export_snapshot(directory: str, snapshot_id: str, output_path: str) -> bool:
    """Export a snapshot to a compressed archive."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    snapshot_data_dir = os.path.join(snap_dir, "data", snapshot_id)
    
    if not os.path.exists(snapshot_data_dir):
        print_error(f"Snapshot '{snapshot_id}' not found")
        return False
    
    # Create tar.gz archive
    import tarfile
    
    if not output_path.endswith('.tar.gz'):
        output_path += '.tar.gz'
    
    try:
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(snapshot_data_dir, arcname=snapshot_id)
        return True
    except Exception as e:
        print_error(f"Failed to export: {e}")
        return False

def import_snapshot(directory: str, archive_path: str) -> Optional[str]:
    """Import a snapshot from a compressed archive."""
    snap_dir = os.path.join(directory, DEFAULT_SNAP_DIR)
    data_dir = os.path.join(snap_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    import tarfile
    
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Get the base directory name
            members = tar.getmembers()
            if not members:
                print_error("Empty archive")
                return None
            
            snapshot_id = members[0].name.split('/')[0]
            tar.extractall(data_dir)
        
        # Load manifest and update config
        manifest = get_snapshot_manifest(directory, snapshot_id)
        if manifest:
            config = load_config(snap_dir)
            config["snapshots"].append({
                "id": manifest["id"],
                "name": manifest.get("name", ""),
                "message": manifest.get("message", ""),
                "created": manifest.get("created", ""),
                "files_count": manifest.get("total_files", 0),
                "total_size": manifest.get("total_size", 0)
            })
            save_config(snap_dir, config)
        
        return snapshot_id
    except Exception as e:
        print_error(f"Failed to import: {e}")
        return None

def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

def print_snapshot_list(snapshots: List[Dict]):
    """Print formatted snapshot list."""
    if not snapshots:
        print_info("No snapshots found")
        return
    
    print(f"\n{colorize('📸 Snapshots', Colors.BOLD)}\n")
    print(f"{'ID':<25} {'Name':<15} {'Files':<8} {'Size':<10} {'Created':<20}")
    print("-" * 80)
    
    for snap in snapshots:
        snap_id = snap.get("id", "")
        name = snap.get("name", "-")
        files = snap.get("files_count", 0)
        size = format_size(snap.get("total_size", 0))
        created = snap.get("created", "")[:19].replace("T", " ")
        
        print(f"{colorize(snap_id, Colors.CYAN):<25} {name:<15} {files:<8} {size:<10} {created:<20}")

def print_diff_result(diff_result: Dict):
    """Print formatted diff result."""
    print(f"\n{colorize('📊 Diff Result', Colors.BOLD)}\n")
    
    if diff_result["added"]:
        print(f"{colorize('Added:', Colors.GREEN)}")
        for path in diff_result["added"]:
            print(f"  + {path}")
    
    if diff_result["removed"]:
        print(f"{colorize('Removed:', Colors.RED)}")
        for path in diff_result["removed"]:
            print(f"  - {path}")
    
    if diff_result["modified"]:
        print(f"{colorize('Modified:', Colors.YELLOW)}")
        for path in diff_result["modified"]:
            print(f"  ~ {path}")
    
    if not any([diff_result["added"], diff_result["removed"], diff_result["modified"]]):
        print_success("No differences found")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='snapcode',
        description='📸 Lightweight Code Snapshot Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  snapcode create my-feature        Create snapshot named 'my-feature'
  snapcode create my-feature -m "Added login feature"  Create with message
  snapcode list                     List all snapshots
  snapcode restore 20260508_120000  Restore from snapshot
  snapcode diff snap1 snap2         Compare two snapshots
  snapcode delete 20260508_120000   Delete a snapshot
  snapcode export snap1 output.tar.gz  Export snapshot
  snapcode import backup.tar.gz     Import snapshot
        """
    )
    
    parser.add_argument('-v', '--version', action='version', version=f'SnapCode v{VERSION}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new snapshot')
    create_parser.add_argument('name', nargs='?', help='Snapshot name')
    create_parser.add_argument('-m', '--message', help='Snapshot message')
    create_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all snapshots')
    list_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from snapshot')
    restore_parser.add_argument('snapshot_id', help='Snapshot ID to restore')
    restore_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    restore_parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Compare two snapshots')
    diff_parser.add_argument('snapshot1', help='First snapshot ID')
    diff_parser.add_argument('snapshot2', help='Second snapshot ID')
    diff_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    diff_parser.add_argument('-f', '--file', help='Show diff for specific file')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a snapshot')
    delete_parser.add_argument('snapshot_id', help='Snapshot ID to delete')
    delete_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export snapshot to archive')
    export_parser.add_argument('snapshot_id', help='Snapshot ID to export')
    export_parser.add_argument('output', help='Output archive path')
    export_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import snapshot from archive')
    import_parser.add_argument('archive', help='Archive path to import')
    import_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show snapshot details')
    info_parser.add_argument('snapshot_id', help='Snapshot ID')
    info_parser.add_argument('-d', '--directory', default='.', help='Target directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    directory = os.path.abspath(getattr(args, 'directory', '.'))
    
    if args.command == 'create':
        name = args.name or ""
        print_info(f"Creating snapshot in {directory}...")
        manifest = create_snapshot(directory, name, args.message or "")
        if manifest:
            print_success(f"Snapshot created: {manifest['id']}")
            print(f"  Files: {manifest['total_files']}")
            print(f"  Size: {format_size(manifest['total_size'])}")
    
    elif args.command == 'list':
        snapshots = list_snapshots(directory)
        print_snapshot_list(snapshots)
    
    elif args.command == 'restore':
        if args.dry_run:
            print_info(f"Dry run: previewing restore from {args.snapshot_id}")
        else:
            print_info(f"Restoring from snapshot {args.snapshot_id}...")
        
        result = restore_snapshot(directory, args.snapshot_id, args.dry_run)
        if result:
            print_success(f"Restored {len(result['restored'])} files")
            if result['errors']:
                print_warning(f"Errors: {len(result['errors'])}")
    
    elif args.command == 'diff':
        diff_result = diff_snapshots(directory, args.snapshot1, args.snapshot2)
        if diff_result:
            if args.file:
                diff_output = show_file_diff(directory, args.snapshot1, args.snapshot2, args.file)
                print(diff_output)
            else:
                print_diff_result(diff_result)
    
    elif args.command == 'delete':
        print_info(f"Deleting snapshot {args.snapshot_id}...")
        if delete_snapshot(directory, args.snapshot_id):
            print_success("Snapshot deleted")
    
    elif args.command == 'export':
        print_info(f"Exporting snapshot {args.snapshot_id}...")
        if export_snapshot(directory, args.snapshot_id, args.output):
            print_success(f"Exported to {args.output}")
    
    elif args.command == 'import':
        print_info(f"Importing snapshot from {args.archive}...")
        snapshot_id = import_snapshot(directory, args.archive)
        if snapshot_id:
            print_success(f"Imported snapshot: {snapshot_id}")
    
    elif args.command == 'info':
        manifest = get_snapshot_manifest(directory, args.snapshot_id)
        if manifest:
            print(f"\n{colorize('📸 Snapshot Info', Colors.BOLD)}\n")
            print(f"ID:       {colorize(manifest['id'], Colors.CYAN)}")
            print(f"Name:     {manifest.get('name', '-')}")
            print(f"Message:  {manifest.get('message', '-')}")
            print(f"Created:  {manifest.get('created', '-')}")
            print(f"Files:    {manifest.get('total_files', 0)}")
            print(f"Size:     {format_size(manifest.get('total_size', 0))}")

if __name__ == '__main__':
    main()
