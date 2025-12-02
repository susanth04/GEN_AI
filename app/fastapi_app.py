"""
Email Classification FastAPI
Milestone 7 - Activity 7.2: Build a FastAPI REST API for predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.predictor import EmailClassifier

# Initialize FastAPI app
app = FastAPI(
    title="Email Classification API",
    description="REST API for classifying emails into Important, Promotion, or Spam categories",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize classifier
classifier = EmailClassifier()


# ============================================
# PYDANTIC MODELS
# ============================================

class EmailRequest(BaseModel):
    """Request model for single email prediction."""
    email: str = Field(..., min_length=1, description="Email text to classify")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "URGENT: Please review the quarterly report by EOD today."
            }
        }


class BatchEmailRequest(BaseModel):
    """Request model for batch email prediction."""
    emails: List[str] = Field(..., min_items=1, max_items=100, 
                               description="List of email texts to classify")


class ConfidenceScores(BaseModel):
    """Model for confidence scores."""
    Important: float
    Promotion: float
    Spam: float


class PredictionResponse(BaseModel):
    """Response model for prediction."""
    success: bool
    predicted_category: Optional[str] = None
    confidence: Optional[float] = None
    confidence_scores: Optional[ConfidenceScores] = None
    preprocessed_text: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str
    model_loaded: bool


# ============================================
# API ROUTES
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main UI page."""
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                             'templates', 'index.html')
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Email Classification API</h1><p>Visit <a href='/docs'>/docs</a> for API documentation.</p>")


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Email Classification API is running!",
        "model_loaded": classifier.model is not None
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(request: EmailRequest):
    """
    Predict the category of a single email.
    
    - **email**: The email text to classify
    
    Returns the predicted category with confidence scores.
    """
    result = classifier.predict(request.email)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))
    
    return result


@app.post("/api/predict/batch")
async def predict_batch(request: BatchEmailRequest):
    """
    Predict categories for multiple emails.
    
    - **emails**: List of email texts to classify (max 100)
    
    Returns predictions for all emails.
    """
    results = classifier.predict_batch(request.emails)
    
    return {
        "success": True,
        "count": len(results),
        "predictions": results
    }


@app.get("/api/categories")
async def get_categories():
    """Get available email categories and their descriptions."""
    return {
        "success": True,
        "categories": ["Urgent", "Financial", "HR", "General"],
        "descriptions": {
            "Urgent": "Time-sensitive, critical matters requiring immediate attention",
            "Financial": "Budget, invoice, payment, and money-related communications",
            "HR": "Human resources, employee, hiring, and benefits related",
            "General": "General business communications and queries"
        }
    }


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("📧 EMAIL CLASSIFICATION FASTAPI SERVER")
    print("="*60)
    print("🌐 Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
