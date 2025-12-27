#!/usr/bin/env python3
"""
Version Creation Script
Creates a timestamped backup of a prompt file in its .versions folder.
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path


def create_version(prompt_file: str) -> str:
    """
    Create a versioned backup of a prompt file.
    
    Args:
        prompt_file: Path to the system_prompt.txt file
        
    Returns:
        Path to the created version file
    """
    prompt_path = Path(prompt_file)
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    if prompt_path.name != 'system_prompt.txt':
        raise ValueError(f"Expected system_prompt.txt, got: {prompt_path.name}")
    
    # Get the .versions directory (sibling of prompt file)
    versions_dir = prompt_path.parent / '.versions'
    versions_dir.mkdir(exist_ok=True)
    
    # Create version filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_filename = f"v_{timestamp}.txt"
    version_path = versions_dir / version_filename
    
    # Copy the current prompt to versions
    shutil.copy2(prompt_path, version_path)
    
    return str(version_path)


def list_versions(prompt_file: str) -> list:
    """
    List all versions of a prompt file.
    
    Args:
        prompt_file: Path to the system_prompt.txt file
        
    Returns:
        List of version files sorted by date (newest first)
    """
    prompt_path = Path(prompt_file)
    versions_dir = prompt_path.parent / '.versions'
    
    if not versions_dir.exists():
        return []
    
    versions = []
    for f in versions_dir.glob('v_*.txt'):
        versions.append({
            'path': str(f),
            'filename': f.name,
            'timestamp': f.stem.replace('v_', ''),
            'size': f.stat().st_size
        })
    
    # Sort by timestamp (newest first)
    versions.sort(key=lambda x: x['timestamp'], reverse=True)
    return versions


def restore_version(version_file: str, prompt_file: str) -> bool:
    """
    Restore a prompt file from a version backup.
    
    Args:
        version_file: Path to the version file to restore
        prompt_file: Path to the system_prompt.txt file
        
    Returns:
        True if successful
    """
    version_path = Path(version_file)
    prompt_path = Path(prompt_file)
    
    if not version_path.exists():
        raise FileNotFoundError(f"Version file not found: {version_file}")
    
    # Create a backup of current before restoring
    if prompt_path.exists():
        create_version(str(prompt_path))
    
    # Restore the version
    shutil.copy2(version_path, prompt_path)
    return True


def main():
    parser = argparse.ArgumentParser(description="Manage prompt versions")
    parser.add_argument("action", choices=['create', 'list', 'restore'],
                       help="Action to perform")
    parser.add_argument("prompt_file", help="Path to system_prompt.txt")
    parser.add_argument("--version", help="Version file to restore (for restore action)")
    
    args = parser.parse_args()
    
    if args.action == 'create':
        version_path = create_version(args.prompt_file)
        print(f"✅ Version created: {version_path}")
        
    elif args.action == 'list':
        versions = list_versions(args.prompt_file)
        if not versions:
            print("No versions found.")
        else:
            print(f"\nVersions for {args.prompt_file}:")
            print("-" * 60)
            for v in versions:
                print(f"  {v['filename']} ({v['size']} bytes)")
                
    elif args.action == 'restore':
        if not args.version:
            print("Error: --version required for restore action")
            sys.exit(1)
        restore_version(args.version, args.prompt_file)
        print(f"✅ Restored from: {args.version}")


if __name__ == "__main__":
    main()

