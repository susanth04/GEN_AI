"""
Email Classification System - Quick Start Script
Run this file to start the FastAPI server
"""

import os
import sys

# Add the project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import fastapi
    except ImportError:
        missing.append('fastapi')
    
    try:
        import uvicorn
    except ImportError:
        missing.append('uvicorn')
    
    try:
        import sklearn
    except ImportError:
        missing.append('scikit-learn')
    
    try:
        import nltk
    except ImportError:
        missing.append('nltk')
    
    if missing:
        print("❌ Missing dependencies:", ', '.join(missing))
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False
    
    return True


def check_nltk_data():
    """Check and download NLTK data if needed."""
    import nltk
    
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("📥 Downloading NLTK data...")
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded!")


def check_model_files():
    """Check if model files exist."""
    model_path = os.path.join(project_root, 'models', 'email_classifier_model.pkl')
    vectorizer_path = os.path.join(project_root, 'models', 'tfidf_vectorizer.pkl')
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print("\nPlease ensure you have the trained model files in the 'models' folder.")
        return False
    
    if not os.path.exists(vectorizer_path):
        print(f"❌ Vectorizer file not found: {vectorizer_path}")
        print("\nPlease ensure you have the TF-IDF vectorizer file in the 'models' folder.")
        return False
    
    return True


def main():
    """Main entry point."""
    print("="*60)
    print("📧 EMAIL CLASSIFICATION SYSTEM")
    print("="*60)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed!")
    
    # Check NLTK data
    print("\n🔍 Checking NLTK data...")
    check_nltk_data()
    print("✅ NLTK data ready!")
    
    # Check model files
    print("\n🔍 Checking model files...")
    if not check_model_files():
        sys.exit(1)
    print("✅ Model files found!")
    
    # Start server
    print("\n" + "="*60)
    print("🚀 Starting FastAPI server...")
    print("="*60)
    print("\n🌐 Web UI:     http://localhost:8000")
    print("📖 API Docs:   http://localhost:8000/docs")
    print("📖 ReDoc:      http://localhost:8000/redoc")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    import uvicorn
    from app.fastapi_app import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
