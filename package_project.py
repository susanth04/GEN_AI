"""
Project Packaging Script
Milestone 10 - Activity 10.4: Prepare final ZIP packaging script
"""

import os
import zipfile
import shutil
from datetime import datetime

# Project configuration
PROJECT_NAME = "Email_Classification_System"
VERSION = "1.0.0"

# Files and folders to include
INCLUDE_ITEMS = [
    'app/',
    'models/',
    'static/',
    'templates/',
    'docs/',
    'requirements.txt',
    'README.md',
    'run.py',
    'package_project.py',
    'Email_Classification_System (2).ipynb'  # Main notebook
]

# Files and folders to exclude
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.pyc',
    '.pyo',
    '.git',
    '.env',
    'venv/',
    '.vscode/',
    '.idea/',
    '*.log',
    'Thumbs.db',
    '.DS_Store'
]


def should_exclude(path):
    """Check if path should be excluded."""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path:
            return True
    return False


def create_zip_package():
    """Create a ZIP package of the project."""
    print("="*60)
    print("📦 EMAIL CLASSIFICATION SYSTEM - PACKAGING")
    print("="*60)
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{PROJECT_NAME}_v{VERSION}_{timestamp}.zip"
    zip_path = os.path.join(project_root, zip_filename)
    
    print(f"\n📁 Project Root: {project_root}")
    print(f"📦 Output File: {zip_filename}")
    
    # Create ZIP file
    print("\n📥 Packaging files...")
    
    files_added = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in INCLUDE_ITEMS:
            item_path = os.path.join(project_root, item)
            
            if os.path.isfile(item_path):
                # Add single file
                if not should_exclude(item_path):
                    arcname = os.path.join(PROJECT_NAME, item)
                    zipf.write(item_path, arcname)
                    print(f"   ✅ {item}")
                    files_added += 1
            
            elif os.path.isdir(item_path):
                # Add directory recursively
                for root, dirs, files in os.walk(item_path):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if not should_exclude(d)]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        if not should_exclude(file_path):
                            # Calculate archive name
                            rel_path = os.path.relpath(file_path, project_root)
                            arcname = os.path.join(PROJECT_NAME, rel_path)
                            zipf.write(file_path, arcname)
                            files_added += 1
                
                print(f"   ✅ {item}")
            
            else:
                print(f"   ⚠️ Not found: {item}")
    
    # Get file size
    file_size = os.path.getsize(zip_path)
    size_mb = file_size / (1024 * 1024)
    
    print("\n" + "="*60)
    print("✅ PACKAGING COMPLETE!")
    print("="*60)
    print(f"\n📦 Package: {zip_filename}")
    print(f"📊 Files Added: {files_added}")
    print(f"💾 Size: {size_mb:.2f} MB")
    print(f"📍 Location: {zip_path}")
    
    return zip_path


def show_project_structure():
    """Display the project structure."""
    print("\n" + "="*60)
    print("📁 PROJECT STRUCTURE")
    print("="*60)
    
    structure = """
Email_Classification_System/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── predictor.py          # Core prediction module
│   ├── fastapi_app.py        # FastAPI REST API
│   └── test_api.py           # API testing script
├── models/
│   ├── email_classifier_model.pkl    # Trained ML model
│   └── tfidf_vectorizer.pkl          # TF-IDF vectorizer
├── static/
│   ├── style.css             # Web UI styles
│   └── script.js             # Frontend JavaScript
├── templates/
│   └── index.html            # Web UI HTML template
├── docs/
│   ├── DOCUMENTATION.md      # Detailed documentation
│   └── screenshots/          # UI screenshots (add manually)
├── Email_Classification_System (2).ipynb  # Training notebook
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── run.py                    # Quick start script
└── package_project.py        # This packaging script
"""
    print(structure)


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("📧 EMAIL CLASSIFICATION SYSTEM")
    print("    Packaging Utility v1.0")
    print("="*60)
    
    # Show structure
    show_project_structure()
    
    # Ask user
    print("\n" + "-"*60)
    response = input("Create ZIP package? (y/n): ").strip().lower()
    
    if response == 'y':
        zip_path = create_zip_package()
        print(f"\n🎉 Your project is ready for submission!")
        print(f"   Submit: {os.path.basename(zip_path)}")
    else:
        print("\n❌ Packaging cancelled.")


if __name__ == "__main__":
    main()
