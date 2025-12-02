/**
 * Email Classification System - Frontend JavaScript
 * Milestone 8: Web App UI - Connect UI to API
 */

// API Configuration
const API_BASE_URL = window.location.origin;

// DOM Elements
const emailInput = document.getElementById('emailInput');
const classifyBtn = document.getElementById('classifyBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const loading = document.getElementById('loading');

// Category icons and colors - 4 categories for organizational efficiency
const categoryConfig = {
    'Urgent': { icon: '🔴', class: 'urgent' },
    'Financial': { icon: '🟡', class: 'financial' },
    'HR': { icon: '🟣', class: 'hr' },
    'General': { icon: '🟢', class: 'general' }
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
    const config = categoryConfig[category] || { icon: '📁', class: '' };
    
    // Update category badge
    const categoryBadge = document.getElementById('categoryBadge');
    const categoryIcon = document.getElementById('categoryIcon');
    const categoryName = document.getElementById('categoryName');
    
    categoryBadge.className = `category-badge ${config.class}`;
    categoryIcon.textContent = config.icon;
    categoryName.textContent = category;
    
    // Update confidence value
    document.getElementById('confidenceValue').textContent = `${confidence}%`;
    
    // Update confidence bars with animation - 4 categories
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
 * Update confidence bar with animation
 */
function updateConfidenceBar(category, score) {
    const bar = document.getElementById(`${category}Bar`);
    const scoreElement = document.getElementById(`${category}Score`);
    
    // Reset bar width
    bar.style.width = '0%';
    
    // Animate after small delay
    setTimeout(() => {
        bar.style.width = `${score}%`;
        scoreElement.textContent = `${score}%`;
    }, 100);
}

/**
 * Show loading spinner
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
    document.getElementById('errorMessage').textContent = `❌ ${message}`;
    errorSection.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Allow Ctrl+Enter to classify
    emailInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            classifyEmail();
        }
    });
    
    // Clear results when input changes
    emailInput.addEventListener('input', () => {
        hideError();
    });
});

// Sample emails for quick testing - 4 categories
const sampleEmails = {
    urgent: "URGENT: Server is down! Need immediate action to restore services. This is critical and requires your attention ASAP!",
    financial: "Please review the Q3 financial report. Budget allocation and invoice approvals are needed for the next fiscal year.",
    hr: "HR Department: New employee onboarding scheduled for Monday. Please complete the training documentation and benefits enrollment.",
    general: "Team meeting rescheduled to Thursday afternoon. Let me know if you can attend."
};

/**
 * Load sample email (can be called from console for testing)
 */
function loadSample(type) {
    if (sampleEmails[type]) {
        emailInput.value = sampleEmails[type];
        hideResults();
        hideError();
    }
}

// Expose functions globally for debugging
window.classifyEmail = classifyEmail;
window.loadSample = loadSample;
