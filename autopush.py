#!/usr/bin/env python3
"""
Auto-commit and push script that watches for file changes.
"""
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Directories to monitor (exclude cache/build directories)
IGNORE_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.pytest_cache', 'db.sqlite3'}
IGNORE_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.so', '.egg-info'}

def get_changed_files():
    """Get list of changed files using git status."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd='/home/emobilis/Desktop/JijiCart',
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting git status: {e}")
        return ""

def should_ignore_file(filepath):
    """Check if file should be ignored."""
    path = Path(filepath)
    
    # Check extension
    if path.suffix in IGNORE_EXTENSIONS:
        return True
    
    # Check if in ignored directories
    for ignore_dir in IGNORE_DIRS:
        if ignore_dir in path.parts:
            return True
    
    return False

def auto_commit_push():
    """Watch for changes and auto-commit/push."""
    last_changes = ""
    consecutive_no_change = 0
    
    print("🚀 Auto-push script started")
    print(f"⏰ Watching directory: /home/emobilis/Desktop/JijiCart")
    print("📝 Will auto-commit and push on file changes\n")
    
    while True:
        time.sleep(2)  # Check every 2 seconds
        
        changes = get_changed_files()
        
        if changes and changes != last_changes:
            # Filter out ignored files
            changed_lines = [line for line in changes.split('\n') if line]
            relevant_changes = [
                line for line in changed_lines 
                if not should_ignore_file(line.split()[-1])
            ]
            
            if relevant_changes:
                print(f"\n✨ Changes detected at {datetime.now().strftime('%H:%M:%S')}:")
                for change in relevant_changes[:5]:  # Show first 5 changes
                    print(f"   {change}")
                if len(relevant_changes) > 5:
                    print(f"   ... and {len(relevant_changes) - 5} more")
                
                try:
                    # Stage all changes
                    subprocess.run(
                        ['git', 'add', '-A'],
                        cwd='/home/emobilis/Desktop/JijiCart',
                        capture_output=True
                    )
                    
                    # Create commit message
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    commit_msg = f"Auto-commit: {timestamp}"
                    
                    # Commit changes
                    result = subprocess.run(
                        ['git', 'commit', '-m', commit_msg],
                        cwd='/home/emobilis/Desktop/JijiCart',
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print("✅ Committed changes")
                        
                        # Push changes
                        push_result = subprocess.run(
                            ['git', 'push'],
                            cwd='/home/emobilis/Desktop/JijiCart',
                            capture_output=True,
                            text=True
                        )
                        
                        if push_result.returncode == 0:
                            print("🚀 Pushed to GitHub")
                        else:
                            print(f"⚠️  Push failed: {push_result.stderr}")
                    else:
                        if "nothing to commit" not in result.stdout:
                            print(f"⚠️  Commit failed: {result.stderr}")
                
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                last_changes = changes
                consecutive_no_change = 0
            else:
                consecutive_no_change += 1
        else:
            consecutive_no_change += 1

if __name__ == '__main__':
    try:
        auto_commit_push()
    except KeyboardInterrupt:
        print("\n\n⛔ Auto-push stopped")
