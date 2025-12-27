#!/usr/bin/env python3
"""
Placeholder Validation Script
Validates that all prompts have valid placeholders and no broken syntax.
"""

import os
import re
import sys
from pathlib import Path


def find_placeholders(content: str) -> list:
    """Extract all {placeholder} patterns from content."""
    return re.findall(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', content)


def find_broken_placeholders(content: str) -> list:
    """Find potentially broken placeholder patterns."""
    issues = []
    
    # Empty placeholders
    if '{}' in content:
        issues.append("Empty placeholder {} found")
    
    # Note: We don't check for nested braces or brace count
    # because prompts may contain YAML/JSON dict strings like {'key': 'value'}
    # which are valid in prompt content
    
    return issues


def validate_prompt_file(filepath: str) -> dict:
    """Validate a single prompt file."""
    result = {
        "file": filepath,
        "valid": True,
        "placeholders": [],
        "issues": []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find placeholders
        result["placeholders"] = find_placeholders(content)
        
        # Check for issues
        issues = find_broken_placeholders(content)
        if issues:
            result["valid"] = False
            result["issues"] = issues
        
        # Check file is not empty
        if len(content.strip()) < 50:
            result["valid"] = False
            result["issues"].append("File appears to be empty or too short")
        
    except Exception as e:
        result["valid"] = False
        result["issues"].append(f"Error reading file: {str(e)}")
    
    return result


def validate_all_prompts(base_dir: str = None) -> dict:
    """Validate all prompt files in the repository."""
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    prompts_dir = os.path.join(base_dir, 'prompts')
    
    results = {
        "total": 0,
        "valid": 0,
        "invalid": 0,
        "files": []
    }
    
    # Find all system_prompt.txt files
    for root, dirs, files in os.walk(prompts_dir):
        for file in files:
            if file == 'system_prompt.txt':
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_dir)
                
                result = validate_prompt_file(filepath)
                result["file"] = rel_path
                results["files"].append(result)
                results["total"] += 1
                
                if result["valid"]:
                    results["valid"] += 1
                else:
                    results["invalid"] += 1
    
    return results


def main():
    """Main entry point."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results = validate_all_prompts(base_dir)
    
    print(f"\n{'='*60}")
    print(f"PLACEHOLDER VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"\nTotal files: {results['total']}")
    print(f"Valid: {results['valid']}")
    print(f"Invalid: {results['invalid']}")
    
    if results['invalid'] > 0:
        print(f"\n{'='*60}")
        print("ISSUES FOUND:")
        print(f"{'='*60}")
        for file_result in results['files']:
            if not file_result['valid']:
                print(f"\n❌ {file_result['file']}")
                for issue in file_result['issues']:
                    print(f"   - {issue}")
    
    print(f"\n{'='*60}")
    print("PLACEHOLDER SUMMARY:")
    print(f"{'='*60}")
    
    all_placeholders = set()
    for file_result in results['files']:
        all_placeholders.update(file_result['placeholders'])
    
    if all_placeholders:
        print(f"\nUnique placeholders found: {len(all_placeholders)}")
        for ph in sorted(all_placeholders):
            print(f"  - {{{ph}}}")
    else:
        print("\nNo placeholders found in any file.")
    
    # Exit with error code if any invalid files
    sys.exit(0 if results['invalid'] == 0 else 1)


if __name__ == "__main__":
    main()

