# Email Classification System - Detailed Documentation

## Milestone 9: Final Documentation

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Data Pipeline](#3-data-pipeline)
4. [Model Details](#4-model-details)
5. [API Reference](#5-api-reference)
6. [Web Interface](#6-web-interface)
7. [Deployment Guide](#7-deployment-guide)
8. [Results & Metrics](#8-results--metrics)
9. [Conclusion](#9-conclusion)
10. [Future Improvements](#10-future-improvements)

---

## 1. Project Overview

### 1.1 Objective
Build an automated email classification system that categorizes incoming emails into three categories:
- **Important**: Work-related, urgent, or high-priority emails
- **Promotion**: Marketing, offers, and promotional content
- **Spam**: Unwanted, suspicious, or potentially harmful emails

### 1.2 Technology Stack
| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.8+ |
| ML Framework | scikit-learn |
| NLP Library | NLTK |
| Web Framework | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Data Format | JSON |
| Model Serialization | Pickle |

### 1.3 Dataset
- **Source**: Enron Email Dataset (Kaggle)
- **Original Size**: 517,401 emails
- **After Cleaning**: 238,370 emails
- **Categories Distribution**:
  - Important: 66.7%
  - Promotion: 23.9%
  - Spam: 9.3%

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EMAIL CLASSIFICATION SYSTEM               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐ │
│  │   Web UI    │────▶│  FastAPI     │────▶│  Predictor   │ │
│  │  (Browser)  │◀────│   Server     │◀────│   Module     │ │
│  └─────────────┘     └──────────────┘     └──────────────┘ │
│                             │                     │         │
│                             ▼                     ▼         │
│                      ┌──────────────┐     ┌──────────────┐ │
│                      │   API        │     │    Model     │ │
│                      │  Endpoints   │     │  + TF-IDF    │ │
│                      └──────────────┘     └──────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Components

1. **Web UI (Frontend)**
   - HTML5 responsive interface
   - CSS3 with modern design
   - JavaScript for API communication

2. **FastAPI Server (Backend)**
   - RESTful API endpoints
   - Request validation
   - CORS middleware
   - Error handling

3. **Predictor Module (ML Engine)**
   - Text preprocessing
   - TF-IDF transformation
   - Model inference
   - Probability scoring

4. **Trained Models**
   - Logistic Regression classifier
   - TF-IDF Vectorizer

---

## 3. Data Pipeline

### 3.1 Data Collection (Milestone 1)
```python
# Download from Kaggle
!kaggle datasets download -d wcukierski/enron-email-dataset
```

### 3.2 Data Cleaning
- Removed 269,529 duplicate emails
- Removed 9,502 short emails (< 50 characters)
- Final dataset: 238,370 emails

### 3.3 Category Assignment (Rule-based)
```python
def assign_category(text):
    text_lower = text.lower()
    
    spam_keywords = ['winner', 'lottery', 'click here', 'urgent', ...]
    promotion_keywords = ['offer', 'discount', 'sale', 'subscribe', ...]
    
    if any(kw in text_lower for kw in spam_keywords):
        return 'Spam'
    elif any(kw in text_lower for kw in promotion_keywords):
        return 'Promotion'
    else:
        return 'Important'
```

### 3.4 Text Preprocessing (Milestone 3)
1. Convert to lowercase
2. Remove email addresses
3. Remove URLs
4. Remove special characters
5. Remove stopwords
6. Apply lemmatization

---

## 4. Model Details

### 4.1 Feature Extraction
- **Method**: TF-IDF Vectorization
- **Max Features**: 5,000
- **N-gram Range**: (1, 2) - Unigrams and Bigrams

### 4.2 Model Training
- **Algorithm**: Logistic Regression
- **Class Weight**: Balanced (handles imbalanced data)
- **Train/Test Split**: 70/30

### 4.3 Hyperparameter Optimization (Milestone 6)
```python
param_grid = {
    'C': [0.1, 1, 10],
    'max_iter': [1000]
}
# Best Parameters: C=10, max_iter=1000
```

### 4.4 Cross-Validation Results
- 5-Fold CV Mean Accuracy: 92.39%
- Standard Deviation: 0.10%

---

## 5. API Reference

### 5.1 Base URL
```
http://localhost:8000
```

### 5.2 Endpoints

#### Health Check
```http
GET /api/health
```
**Response:**
```json
{
    "status": "healthy",
    "message": "Email Classification API is running!",
    "model_loaded": true
}
```

#### Classify Email
```http
POST /api/predict
Content-Type: application/json
```
**Request Body:**
```json
{
    "email": "Please submit your quarterly report by Friday."
}
```
**Response:**
```json
{
    "success": true,
    "predicted_category": "Important",
    "confidence": 87.5,
    "confidence_scores": {
        "Important": 87.5,
        "Promotion": 8.2,
        "Spam": 4.3
    },
    "preprocessed_text": "please submit quarterly report friday"
}
```

#### Batch Classification
```http
POST /api/predict/batch
Content-Type: application/json
```
**Request Body:**
```json
{
    "emails": [
        "Meeting tomorrow at 9 AM",
        "50% off sale this weekend!",
        "You won a million dollars!"
    ]
}
```

#### Get Categories
```http
GET /api/categories
```

---

## 6. Web Interface

### 6.1 Features
- Clean, modern design with gradient background
- Real-time email classification
- Visual confidence score bars
- Responsive design for mobile devices
- Error handling with user-friendly messages

### 6.2 Screenshots

#### Main Interface
![Main UI](screenshots/main_ui_placeholder.png)
*Description: The main interface with email input textbox and classify button*

#### Classification Results
![Results](screenshots/results_placeholder.png)
*Description: Classification results showing category and confidence scores*

#### Mobile View
![Mobile](screenshots/mobile_placeholder.png)
*Description: Responsive design on mobile devices*

---

## 7. Deployment Guide

### 7.1 Local Deployment

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 3. Run the server
python run.py
# OR
uvicorn app.fastapi_app:app --host 0.0.0.0 --port 8000
```

### 7.2 Production Deployment (with Gunicorn)

```bash
gunicorn app.fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 7.3 Docker Deployment (Future)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
CMD ["uvicorn", "app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 8. Results & Metrics

### 8.1 Model Performance Summary

| Metric | Original Model | Optimized Model |
|--------|---------------|-----------------|
| Accuracy | 92.79% | **94.02%** |
| Improvement | - | +1.23% |

### 8.2 Classification Report (Optimized Model)

```
              precision    recall  f1-score   support

   Important       0.95      0.99      0.97     47722
   Promotion       0.92      0.88      0.90     17084
        Spam       0.92      0.74      0.82      6705

    accuracy                           0.94     71511
   macro avg       0.93      0.87      0.90     71511
weighted avg       0.94      0.94      0.94     71511
```

### 8.3 Confusion Matrix

```
                 Predicted
              Imp   Promo   Spam
Actual Imp   47195   386    141
       Promo  1531  14993   560
       Spam   1150   580   4975
```

---

## 9. Conclusion

### 9.1 Achievements
✅ Successfully built an end-to-end email classification system
✅ Achieved 94.02% accuracy on the Enron Email Dataset
✅ Implemented RESTful API with FastAPI
✅ Created user-friendly web interface
✅ Comprehensive documentation and testing

### 9.2 Key Learnings
- Text preprocessing is crucial for NLP tasks
- Class imbalance handling improves model performance
- GridSearchCV helps find optimal hyperparameters
- FastAPI provides excellent performance and documentation

### 9.3 Challenges Overcome
1. Handling large dataset (500K+ emails)
2. Dealing with class imbalance
3. Text cleaning and preprocessing
4. API design and error handling

---

## 10. Future Improvements

### 10.1 Short-term
1. Add more email categories (Social, Updates, Forums)
2. Implement email threading support
3. Add user feedback loop for model improvement

### 10.2 Medium-term
1. **Deep Learning Models**
   - LSTM for sequence modeling
   - BERT for contextual embeddings
   - Transformer-based classification

2. **Additional Features**
   - Sender reputation scoring
   - Attachment analysis
   - Header analysis

### 10.3 Long-term
1. **Email Service Integration**
   - Gmail API integration
   - Outlook/Microsoft 365 integration
   - IMAP/SMTP support

2. **Cloud Deployment**
   - AWS Lambda for serverless
   - Kubernetes for scaling
   - CI/CD pipeline

3. **Advanced Features**
   - Multi-language support
   - Custom category training
   - Real-time streaming classification

---

## Appendix

### A. File Descriptions

| File | Description |
|------|-------------|
| `app/predictor.py` | Core prediction module with EmailClassifier class |
| `app/fastapi_app.py` | FastAPI application with REST endpoints |
| `app/test_api.py` | API testing script with sample requests |
| `models/*.pkl` | Trained model and vectorizer files |
| `templates/index.html` | Web UI HTML template |
| `static/style.css` | CSS styles for web interface |
| `static/script.js` | Frontend JavaScript for API communication |

### B. API Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Endpoint not found |
| 500 | Internal server error |

### C. Contact

For questions or support, please refer to the project repository.

---

*Documentation generated for Email Classification System v1.0*
*Last updated: December 2024*
