/**
 * Email Classification System - Frontend JavaScript
 * Vercel Deployment Version
 */

// API Configuration - UPDATE THIS AFTER DEPLOYING BACKEND TO RENDER
const API_BASE_URL = 'https://your-render-app-name.onrender.com';

// DOM Elements
const emailInput = document.getElementById('emailInput');
const classifyBtn = document.getElementById('classifyBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const loading = document.getElementById('loading');

// Category config
const categoryConfig = {
    'Urgent': { class: 'urgent' },
    'Financial': { class: 'financial' },
    'HR': { class: 'hr' },
    'General': { class: 'general' }
};

/**
 * Classify email using the API
 */
async function classifyEmail() {
    const emailText = emailInput.value.trim();
    
    // Validate input
    if (!emailText) {
        showError('Please enter email content to classify.');
        return;
    }
    
    // Show loading, hide results
    showLoading(true);
    hideResults();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: emailText })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults(data);
        } else {
            showError(data.error || data.detail || 'Classification failed. Please try again.');
        }
    } catch (error) {
        console.error('API Error:', error);
        showError('Failed to connect to the server. Please ensure the API is running.');
    } finally {
        showLoading(false);
    }
}

/**
 * Display classification results
 */
function displayResults(data) {
    const category = data.predicted_category;
    const confidence = data.confidence;
    const scores = data.confidence_scores;
    
    // Get category config
    const config = categoryConfig[category] || { class: '' };
    
    // Update category badge
    const categoryBadge = document.getElementById('categoryBadge');
    const categoryName = document.getElementById('categoryName');
    
    categoryBadge.className = `category-badge ${config.class}`;
    categoryName.textContent = category;
    
    // Update confidence value
    document.getElementById('confidenceValue').textContent = `${confidence}%`;
    
    // Update confidence bars
    updateConfidenceBar('urgent', scores.Urgent || 0);
    updateConfidenceBar('financial', scores.Financial || 0);
    updateConfidenceBar('hr', scores.HR || 0);
    updateConfidenceBar('general', scores.General || 0);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Update a confidence bar
 */
function updateConfidenceBar(category, score) {
    const bar = document.getElementById(`${category}Bar`);
    const scoreEl = document.getElementById(`${category}Score`);
    
    if (bar && scoreEl) {
        bar.style.width = `${score}%`;
        scoreEl.textContent = `${score}%`;
    }
}

/**
 * Show loading state
 */
function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
    classifyBtn.disabled = show;
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

// Allow Enter key to submit
emailInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        classifyEmail();
    }
});
