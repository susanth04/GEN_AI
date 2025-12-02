"""
Email Classification Predictor Module
Milestone 7 - Activity 7.1: Robust Prediction Function
"""

import pickle
import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

class EmailClassifier:
    """
    A robust email classification predictor that loads trained model
    and vectorizer to classify emails into categories.
    """
    
    def __init__(self, model_path=None, vectorizer_path=None):
        """
        Initialize the classifier with model and vectorizer paths.
        
        Args:
            model_path: Path to the trained model pickle file
            vectorizer_path: Path to the TF-IDF vectorizer pickle file
        """
        # Default paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if model_path is None:
            model_path = os.path.join(base_dir, 'models', 'email_classifier_model.pkl')
        if vectorizer_path is None:
            vectorizer_path = os.path.join(base_dir, 'models', 'tfidf_vectorizer.pkl')
        
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Category labels - 4 classes for organizational efficiency
        self.categories = ['Urgent', 'Financial', 'HR', 'General']
        
        # Load model and vectorizer
        self.load_model()
    
    def load_model(self):
        """Load the trained model and vectorizer from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            print("✅ Model and vectorizer loaded successfully!")
            return True
        except FileNotFoundError as e:
            print(f"❌ Error loading model files: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def preprocess_text(self, text):
        """
        Preprocess email text for classification.
        
        Args:
            text: Raw email text
            
        Returns:
            Cleaned and preprocessed text
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and remove stopwords
        words = text.split()
        words = [self.lemmatizer.lemmatize(word) for word in words 
                 if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(words)
    
    def predict(self, email_text):
        """
        Predict the category of an email.
        
        Args:
            email_text: The email content to classify
            
        Returns:
            dict: Contains predicted category, confidence scores, and probabilities
        """
        if self.model is None or self.vectorizer is None:
            return {
                'success': False,
                'error': 'Model not loaded. Please check model files.'
            }
        
        try:
            # Preprocess the email
            cleaned_text = self.preprocess_text(email_text)
            
            if not cleaned_text:
                return {
                    'success': False,
                    'error': 'Email text is empty after preprocessing.'
                }
            
            # Transform using TF-IDF
            text_vectorized = self.vectorizer.transform([cleaned_text])
            
            # Get prediction and probabilities
            prediction = self.model.predict(text_vectorized)[0]
            probabilities = self.model.predict_proba(text_vectorized)[0]
            
            # Create confidence scores dictionary
            confidence_scores = {
                cat: round(prob * 100, 2) 
                for cat, prob in zip(self.categories, probabilities)
            }
            
            # Get the maximum confidence
            max_confidence = max(probabilities) * 100
            
            return {
                'success': True,
                'predicted_category': prediction,
                'confidence': round(max_confidence, 2),
                'confidence_scores': confidence_scores,
                'preprocessed_text': cleaned_text[:200] + '...' if len(cleaned_text) > 200 else cleaned_text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_batch(self, emails):
        """
        Predict categories for multiple emails.
        
        Args:
            emails: List of email texts
            
        Returns:
            List of prediction results
        """
        return [self.predict(email) for email in emails]


# Quick test function
def test_predictor():
    """Test the predictor with sample emails."""
    classifier = EmailClassifier()
    
    test_emails = [
        "URGENT: Server is down! Need immediate action to restore services.",
        "Please review the Q3 financial report and budget allocation.",
        "HR Department: New employee onboarding scheduled for Monday.",
        "Team meeting rescheduled to Thursday afternoon."
    ]
    
    print("\n" + "="*60)
    print("EMAIL CLASSIFICATION TEST (4 Categories)")
    print("="*60)
    
    for i, email in enumerate(test_emails, 1):
        result = classifier.predict(email)
        print(f"\n📧 Email {i}: {email[:50]}...")
        if result['success']:
            print(f"   Category: {result['predicted_category']}")
            print(f"   Confidence: {result['confidence']}%")
            print(f"   Scores: {result['confidence_scores']}")
        else:
            print(f"   Error: {result['error']}")


if __name__ == "__main__":
    test_predictor()
