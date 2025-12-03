@app.post("/api/predict")
async def predict_email(request: EmailRequest):
    # Preprocess email
    cleaned_text = predictor.preprocess_text(request.email)
    
    # Transform and predict
    text_vectorized = vectorizer.transform([cleaned_text])
    prediction = model.predict(text_vectorized)[0]
    probabilities = model.predict_proba(text_vectorized)[0]
    
    # Return results
    return {
        "success": True,
        "predicted_category": prediction,
        "confidence": max(probabilities) * 100,
        "confidence_scores": {...}
    }