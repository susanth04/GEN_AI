# Email Classification System for Organizational Efficiency

## 📋 Project Overview

An AI-powered email classification system that automatically categorizes emails into **Important**, **Promotion**, or **Spam** categories using Machine Learning. Built using the Enron Email Dataset and deployed with FastAPI.

![Project Banner](docs/screenshots/banner_placeholder.png)

---

## 🎯 Features

- **Automatic Email Classification**: Classify emails into 3 categories with high accuracy
- **REST API**: FastAPI-based REST API for predictions
- **Web Interface**: User-friendly web UI for email classification
- **Batch Processing**: Classify multiple emails at once
- **Real-time Predictions**: Get instant classification results with confidence scores

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 94.02% |
| **Model** | Logistic Regression (Optimized) |
| **Dataset** | Enron Email Dataset (238,370 emails) |
| **Feature Extraction** | TF-IDF (5,000 features) |

### Classification Report

| Category | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Important | 0.95 | 0.99 | 0.97 |
| Promotion | 0.92 | 0.88 | 0.90 |
| Spam | 0.92 | 0.74 | 0.82 |

---

## 🏗️ Project Structure

```
GENAI_PROJ/
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
│   └── screenshots/          # UI screenshots
├── notebooks/
│   └── Email_Classification_System.ipynb  # Training notebook
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── run.py                    # Quick start script
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone/Download the project**
   ```bash
   cd GENAI_PROJ
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
   ```

### Running the Application

**Option 1: Quick Start Script**
```bash
python run.py
```

**Option 2: Run FastAPI directly**
```bash
cd app
python fastapi_app.py
```

**Option 3: Using uvicorn**
```bash
uvicorn app.fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Application

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

### Classify Single Email
```http
POST /api/predict
Content-Type: application/json

{
    "email": "Your email content here..."
}
```

**Response:**
```json
{
    "success": true,
    "predicted_category": "Important",
    "confidence": 95.5,
    "confidence_scores": {
        "Important": 95.5,
        "Promotion": 3.2,
        "Spam": 1.3
    }
}
```

### Batch Classification
```http
POST /api/predict/batch
Content-Type: application/json

{
    "emails": ["Email 1...", "Email 2...", "Email 3..."]
}
```

### Get Categories
```http
GET /api/categories
```

---

## 🧪 Testing

### Run API Tests
```bash
# Start the server first, then in another terminal:
python app/test_api.py
```

### Test with curl
```bash
# Health check
curl http://localhost:8000/api/health

# Classify email
curl -X POST http://localhost:8000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"email": "URGENT: Meeting at 10 AM tomorrow"}'
```

---

## 📸 Screenshots

### Web Interface
![Web UI](docs/screenshots/web_ui_placeholder.png)

### Classification Results
![Results](docs/screenshots/results_placeholder.png)

### API Documentation
![API Docs](docs/screenshots/api_docs_placeholder.png)

---

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Server settings
HOST=0.0.0.0
PORT=8000

# Model paths (if different from default)
MODEL_PATH=models/email_classifier_model.pkl
VECTORIZER_PATH=models/tfidf_vectorizer.pkl
```

---

## 📈 Model Training

The model was trained using the Jupyter notebook in `notebooks/Email_Classification_System.ipynb`.

### Training Process:
1. **Data Collection**: Enron Email Dataset from Kaggle (517,401 emails)
2. **Data Cleaning**: Removed duplicates and short emails (238,370 remaining)
3. **Text Preprocessing**: Lowercase, stopword removal, lemmatization
4. **Feature Extraction**: TF-IDF Vectorization (5,000 features)
5. **Model Training**: Logistic Regression with GridSearchCV
6. **Optimization**: Best parameters - C=10, max_iter=1000

---

## 🔮 Future Improvements

1. **Deep Learning Models**: Implement LSTM or BERT for better accuracy
2. **More Categories**: Add custom category support
3. **Email Integration**: Connect with Gmail/Outlook APIs
4. **Real-time Processing**: Add WebSocket support for streaming
5. **Docker Deployment**: Containerize for easy deployment
6. **Cloud Hosting**: Deploy to AWS/GCP/Azure

---

## 👥 Contributors

- **Student Name** - Development & Implementation

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- Enron Email Dataset (Kaggle)
- scikit-learn library
- FastAPI framework
- NLTK for text processing

---

## 📞 Support

For questions or issues, please create an issue in the repository.

---

*Built with ❤️ using Python, FastAPI, and Machine Learning*
