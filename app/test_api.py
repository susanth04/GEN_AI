"""
API Testing Script
Milestone 7 - Activity 7.3: Test API endpoint with sample requests
"""

import requests
import json

# API Base URL (change port for Flask vs FastAPI)
FLASK_URL = "http://localhost:5000"
FASTAPI_URL = "http://localhost:8000"

# Use Flask by default
BASE_URL = FLASK_URL


def test_health_check():
    """Test the health check endpoint."""
    print("\n" + "="*50)
    print("🔍 Testing Health Check Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_single_prediction():
    """Test single email prediction endpoint."""
    print("\n" + "="*50)
    print("📧 Testing Single Prediction Endpoint")
    print("="*50)
    
    test_cases = [
        {
            "name": "Important Email",
            "email": "URGENT: The quarterly meeting is scheduled for tomorrow at 10 AM. Please review the attached report and come prepared with your updates."
        },
        {
            "name": "Promotion Email",
            "email": "🎉 FLASH SALE! Get 50% off on all products this weekend only! Use code SAVE50 at checkout. Limited time offer!"
        },
        {
            "name": "Spam Email",
            "email": "Congratulations!!! You have been selected as the winner of $5,000,000! Click here immediately to claim your prize. Act now!"
        }
    ]
    
    for test in test_cases:
        print(f"\n📌 Test: {test['name']}")
        print(f"   Email: {test['email'][:60]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict",
                json={"email": test['email']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Predicted: {result.get('predicted_category')}")
                print(f"   📊 Confidence: {result.get('confidence')}%")
                print(f"   📈 Scores: {result.get('confidence_scores')}")
            else:
                print(f"   ❌ Error: {response.json()}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")


def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\n" + "="*50)
    print("📦 Testing Batch Prediction Endpoint")
    print("="*50)
    
    emails = [
        "Please submit your timesheet by Friday.",
        "Buy one get one free! Today only!",
        "You've won a lottery! Send your bank details.",
        "Team meeting rescheduled to 3 PM.",
        "Exclusive discount just for you!"
    ]
    
    print(f"Sending {len(emails)} emails for batch classification...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/batch",
            json={"emails": emails},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch processed successfully!")
            print(f"📊 Total predictions: {result.get('count')}")
            
            for i, pred in enumerate(result.get('predictions', []), 1):
                if pred.get('success'):
                    print(f"   Email {i}: {pred['predicted_category']} ({pred['confidence']}%)")
                else:
                    print(f"   Email {i}: Error - {pred.get('error')}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")


def test_categories():
    """Test categories endpoint."""
    print("\n" + "="*50)
    print("📂 Testing Categories Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/categories")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_error_handling():
    """Test error handling."""
    print("\n" + "="*50)
    print("⚠️ Testing Error Handling")
    print("="*50)
    
    # Test empty email
    print("\n📌 Test: Empty email")
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json={"email": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test missing email field
    print("\n📌 Test: Missing email field")
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")


def run_all_tests():
    """Run all API tests."""
    print("\n" + "="*60)
    print("🚀 EMAIL CLASSIFICATION API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    
    # Run tests
    test_health_check()
    test_categories()
    test_single_prediction()
    test_batch_prediction()
    test_error_handling()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    # You can switch between Flask and FastAPI by changing BASE_URL
    # BASE_URL = FASTAPI_URL  # Uncomment for FastAPI
    
    run_all_tests()
