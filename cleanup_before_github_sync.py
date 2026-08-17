python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup script before GitHub sync
Removes redundant folders and files
"""
import os
import sys
import shutil
from pathlib import Path

# Enable UTF-8 for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

def cleanup_project():
    """Remove redundant files and folders before GitHub sync"""
    
    project_root = Path(__file__).parent
    items_to_remove = []
    
    print("🧹 MAHALO Project Cleanup - Pre-GitHub Sync\n")
    print("=" * 60)
    
    # 1. Check for nested MAHALO folder and remove it immediately
    mahalo_nested = project_root / "MAHALO"
    if mahalo_nested.exists():
        try:
            shutil.rmtree(mahalo_nested)
            print(f"✅ Removed nested MAHALO folder")
                except Exception as e:
            print(f"❌ Error removing MAHALO folder: {e}")
            
    # 2. Check for .venv (should not be in GitHub)
    venv_folder = project_root / ".venv"
    if venv_folder.exists() and venv_folder.is_dir():
        print("⚠️  Found .venv folder - checking .gitignore...")
    gitignore = project_root / ".gitignore"
    if gitignore.exists():
        with open(gitignore, 'r') as f:
                gitignore_content = f.read()
                if '.venv' not in gitignore_content and 'venv/' not in gitignore_content:
                    print("  Adding .venv to .gitignore")
                    with open(gitignore, 'a') as f:
                        f.write("\n.venv/\n")
        print("  ✓ .venv will be ignored by git\n")
    
    # 3. Check for database files (should not be in GitHub)
    db_file = project_root / "mahalo.db"
    if db_file.exists():
        print("⚠️  Found mahalo.db - checking .gitignore...")
        gitignore = project_root / ".gitignore"
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                gitignore_content = f.read()
                if 'mahalo.db' not in gitignore_content:
                    print("  ✓ mahalo.db already in .gitignore\n")
                else:
                    print("  ✓ mahalo.db already in .gitignore\n")
    
    # 4. Check for node_modules (should not be in GitHub)
    frontend_node_modules = project_root / "frontend" / "node_modules"
    if frontend_node_modules.exists():
        print("⚠️  Found frontend/node_modules")
        print("  ✓ Already in .gitignore\n")
    
    # 5. Check for __pycache__ folders
    pycache_folders = list(project_root.rglob("__pycache__"))
    if pycache_folders:
        print(f"⚠️  Found {len(pycache_folders)} __pycache__ folders")
        print("  ✓ Already in .gitignore\n")
    
    # Display summary
    if items_to_remove:
        print("\n📋 Items to remove:")
        print("-" * 60)
        for item_type, item_path, reason in items_to_remove:
            print(f"\n{item_type.upper()}: {item_path.name}")
            print(f"  Location: {item_path.relative_to(project_root)}")
            print(f"  Reason: {reason}")
        print("\n" + "=" * 60)
        response = input("\n🗑️  Remove these items? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            print("\n🔄 Removing items...\n")
            for item_type, item_path, reason in items_to_remove:
                try:
                    if item_path.is_dir():
                        shutil.rmtree(item_path)
                        print(f"  ✅ Removed: {item_path.name}/")
                    else:
                        item_path.unlink()
                        print(f"  ✅ Removed: {item_path.name}")
                except Exception as e:
                    print(f"  ❌ Error removing {item_path.name}: {e}")
            
            print("\n✅ Cleanup complete!")
        else:
            print("\n❌ Cleanup cancelled - no changes made")
    else:
        print("\n✅ No redundant files found - project is clean!")
    
    # Show .gitignore status
    print("\n" + "=" * 60)
    print("📝 .gitignore Status:")
    print("-" * 60)
    gitignore = project_root / ".gitignore"
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            ignored_items = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print("Currently ignoring:")
            for item in ignored_items:
                print(f"  • {item}")
    print("\n" + "=" * 60)
    
    # Show recommended next steps
    print("\n📋 Recommended Next Steps:")
    print("-" * 60)
    print("1. Review the cleanup results above")
    print("2. Run: git init")
    print("3. Run: git remote add origin https://github.com/tjblavakumar/mahalo.git")
    print("4. Run: git add .")
    print("5. Run: git commit -m 'Initial commit - clean project structure'")
    print("6. Run: git push -u origin main --force")
    print("\n" + "=" * 60)
    print("✅ Ready for GitHub sync!")

if __name__ == "__main__":
    try:
        cleanup_project()
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error during cleanup: {e}")

