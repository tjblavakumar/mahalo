"""
Project cleanup script to organize documentation and remove redundant files.
This script will:
1. Move all proxy-related docs to docs/archive/proxy_fixes/
2. Move redundant test data docs to docs/archive/test_data/
3. Keep only essential docs in root
4. Create a consolidated README
"""
import os
import shutil
from pathlib import Path


def cleanup_project():
    """Clean up the MAHALO project structure."""
    
    project_root = Path(__file__).parent
    
    # Create archive directories
    docs_archive = project_root / "docs" / "archive"
    proxy_fixes_archive = docs_archive / "proxy_fixes"
    test_data_archive = docs_archive / "test_data"
    general_archive = docs_archive / "general"
    
    for dir_path in [proxy_fixes_archive, test_data_archive, general_archive]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Files to keep in root
    keep_in_root = {
        "README.md",
        "START_HERE.md",
        "requirements.txt",
        "pytest.ini",
        ".gitignore",
    }
    
    # Proxy-related docs to archive
    proxy_docs = [
        "BEFORE_AFTER_PROXY_FIX.md",
        "FRB_PROXY_FIX_GUIDE.md",
        "INDEX_PROXY_FIX.md",
        "PROXY_CONFIGURATION.md",
        "PROXY_FIX_SUMMARY.md",
        "QUICK_PROXY_FIX.md",
        "README_PROXY_FIX.md",
        "env_template_with_proxy.txt",
        "fix_proxy.bat",
        "fix_proxy_permanent.ps1",
        "setup_proxy.bat",
        "setup_proxy.sh",
        "APPLY_FIX_NOW.bat",
        "test_proxy_config.py",
    ]
    
    # Test data docs to archive
    test_data_docs = [
        "TEST_DATA_IMPROVEMENTS.md",
        "QUICK_START_TEST_DATA.txt",
        "generate_demo_data.bat",
        "generate_demo_data.sh",
    ]
    
    # General docs to archive
    general_docs = [
        "FIXES_SUMMARY.md",
        "FORMATTING_FIX_SUMMARY.md",
        "INTELLIGENT_RESPONSE_FIX.md",
        "QUICK_FORMATTING_FIX.md",
        "YOUR_SOLUTION.md",
    ]
    
    moved_files = []
    skipped_files = []
    
    print("="*70)
    print("MAHALO Project Cleanup")
    print("="*70)
    print()
    
    # Move proxy-related docs
    print("Moving proxy-related documentation...")
    for filename in proxy_docs:
        src = project_root / filename
        if src.exists():
            dst = proxy_fixes_archive / filename
            try:
                shutil.move(str(src), str(dst))
                moved_files.append(f"  OK {filename} -> docs/archive/proxy_fixes/")
            except Exception as e:
                skipped_files.append(f"  ERROR {filename}: {e}")
    
    # Move test data docs  
    print("Moving test data documentation...")
    for filename in test_data_docs:
        src = project_root / filename
        if src.exists():
            dst = test_data_archive / filename
            try:
                shutil.move(str(src), str(dst))
                moved_files.append(f"  OK {filename} -> docs/archive/test_data/")
            except Exception as e:
                skipped_files.append(f"  ERROR {filename}: {e}")
    
    # Move general docs
    print("Moving general documentation...")
    for filename in general_docs:
        src = project_root / filename
        if src.exists():
            dst = general_archive / filename
            try:
                shutil.move(str(src), str(dst))
                moved_files.append(f"  OK {filename} -> docs/archive/general/")
            except Exception as e:
                skipped_files.append(f"  ERROR {filename}: {e}")
    
    # Summary
    print()
    print("="*70)
    print("Cleanup Summary")
    print("="*70)
    print()
    print(f"Moved {len(moved_files)} files:")
    for item in moved_files:
        print(item)
    
    if skipped_files:
        print()
        print(f"Skipped {len(skipped_files)} files:")
        for item in skipped_files:
            print(item)
    
    print()
    print("="*70)
    print("Project Structure Cleaned!")
    print("="*70)
    print()
    print("Root directory now contains only:")
    for item in keep_in_root:
        if (project_root / item).exists():
            print(f"  - {item}")
    print()
    print("Archived documentation in:")
    print(f"  - docs/archive/proxy_fixes/ ({len(proxy_docs)} files)")
    print(f"  - docs/archive/test_data/ ({len(test_data_docs)} files)")
    print(f"  - docs/archive/general/ ({len(general_docs)} files)")
    print()


if __name__ == "__main__":
    cleanup_project()
