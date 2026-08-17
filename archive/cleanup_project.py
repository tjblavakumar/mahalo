"""
Cleanup script to organize the MAHALO project.
Moves unnecessary MD files and test scripts to an archive folder.
"""
import os
import shutil
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).parent

# Files to keep in root
KEEP_IN_ROOT = {
    'README.md',
    'requirements.txt',
    'pytest.ini',
    '.gitignore',
    '.env',
    'mahalo.db'
}

# Create archive directory
ARCHIVE_DIR = BASE_DIR / 'archive'
ARCHIVE_DIR.mkdir(exist_ok=True)

# Files to move (all the summary/fix MD files)
MD_FILES_TO_ARCHIVE = [
    'AGENT_QUERY_FIXES.md',
    'ALL_FOUR_BUGS_MASTER_SUMMARY.md',
    'BUG_ANALYSIS_SUMMARY.md',
    'COMPLETE_FIX_SUMMARY.md',
    'COMPOUND_QUERY_FIX.md',
    'CONTEXT_AWARENESS_FIXES_SUMMARY.md',
    'ELABORATION_REQUEST_FIX.md',
    'FINAL_ANALYSIS_SUMMARY.md',
    'FIX_SUMMARY.md',
    'FORMAT_RESPONSE_FIX.md',
    'IMPLEMENTATION_CHECKLIST.md',
    'IMPLEMENTATION_COMPLETE.md',
    'IMPLEMENTATION_GUIDE.md',
    'LLM_USAGE_ARCHITECTURE.md',
    'ORCHESTRATOR_ELABORATE_FIX.md',
    'QUICK_REFERENCE.md',
    'QUICK_TEST_GUIDE.md',
    'RESTART_INSTRUCTIONS.md',
    'SMART_ORCHESTRATOR_UPGRADE.md',
    'SPLUNK_QUERY_FIX.md',
    'STORY_DRAFTING_ASSISTANCE_FIX.md',
    'THREE_BUGS_VISUAL_SUMMARY.md',
    'TROUBLESHOOTING_DATABASE_FIX.md',
    'VISUAL_FLOW_DIAGRAMS.md'
]

# Test scripts to move (keep only the official tests in tests/ directory)
TEST_SCRIPTS_TO_ARCHIVE = [
    'test_agents.py',
    'test_all_agents.py',
    'test_compound_query_fix.py',
    'test_executive_overview.py',
    'test_http.py',
    'test_production_query_fix.py',
    'test_proxy.py',
    'test_splunk_queries.py'
]

def move_to_archive(filename):
    """Move a file to the archive directory."""
    source = BASE_DIR / filename
    if source.exists():
        dest = ARCHIVE_DIR / filename
        try:
            shutil.move(str(source), str(dest))
            print(f"✓ Moved: {filename}")
            return True
        except Exception as e:
            print(f"✗ Error moving {filename}: {e}")
            return False
    else:
        print(f"- Skipped (not found): {filename}")
        return False

def main():
    print("=" * 70)
    print("MAHALO Project Cleanup")
    print("=" * 70)
    print()
    
    # Move MD documentation files
    print("Moving documentation files to archive...")
    print("-" * 70)
    moved_md = 0
    for md_file in MD_FILES_TO_ARCHIVE:
        if move_to_archive(md_file):
            moved_md += 1
    print()
    
    # Move test scripts
    print("Moving test scripts to archive...")
    print("-" * 70)
    moved_tests = 0
    for test_file in TEST_SCRIPTS_TO_ARCHIVE:
        if move_to_archive(test_file):
            moved_tests += 1
    print()
    
    # Summary
    print("=" * 70)
    print("Cleanup Summary")
    print("=" * 70)
    print(f"✓ Moved {moved_md} documentation files")
    print(f"✓ Moved {moved_tests} test scripts")
    print(f"✓ Files archived in: {ARCHIVE_DIR}")
    print()
    print("Remaining root files:")
    print("-" * 70)
    for item in sorted(BASE_DIR.iterdir()):
        if item.is_file() and not item.name.startswith('.'):
            print(f"  - {item.name}")
    print()
    print("✓ Cleanup complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
