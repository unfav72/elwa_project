// ELWA - Tech X Espadas - JavaScript

// Global state
let currentUser = null;
let aiTutorActive = false;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeMenu();
    initializeAITutor();
    setupBackgroundAnimation();
});

// Menu Toggle
function initializeMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sideMenu = document.querySelector('.side-menu');
    const overlay = document.createElement('div');
    overlay.className = 'menu-overlay';
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sideMenu.classList.toggle('active');
            
            if (sideMenu.classList.contains('active')) {
                document.body.appendChild(overlay);
                overlay.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    z-index: 998;
                `;
                overlay.addEventListener('click', closeMenu);
            } else {
                if (overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                }
            }
        });
    }
    
    function closeMenu() {
        sideMenu.classList.remove('active');
        if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
    }
}

// AI Tutor
function initializeAITutor() {
    const tutorBtn = document.querySelector('.ai-tutor-btn');
    const tutorPopup = document.querySelector('.ai-tutor-popup');
    const tutorClose = document.querySelector('.tutor-close');
    const tutorSend = document.querySelector('.tutor-send');
    const tutorInput = document.querySelector('.tutor-input');
    
    if (tutorBtn) {
        tutorBtn.addEventListener('click', function() {
            tutorPopup.classList.toggle('active');
            aiTutorActive = !aiTutorActive;
        });
    }
    
    if (tutorClose) {
        tutorClose.addEventListener('click', function() {
            tutorPopup.classList.remove('active');
            aiTutorActive = false;
        });
    }
    
    if (tutorSend) {
        tutorSend.addEventListener('click', sendTutorMessage);
    }
    
    if (tutorInput) {
        tutorInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendTutorMessage();
            }
        });
    }
}

async function sendTutorMessage() {
    const input = document.querySelector('.tutor-input');
    const messagesContainer = document.querySelector('.tutor-messages');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addTutorMessage(message, 'user');
    input.value = '';
    
    // Show loading
    const loadingMsg = addTutorMessage('<div class="loading"></div>', 'ai');
    
    try {
        const response = await fetch('/ai_tutor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove loading message
        loadingMsg.remove();
        
        if (data.success) {
            addTutorMessage(data.response, 'ai');
        } else {
            addTutorMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
    } catch (error) {
        loadingMsg.remove();
        addTutorMessage('Connection error. Please check your internet connection.', 'ai');
    }
}

function addTutorMessage(text, sender) {
    const messagesContainer = document.querySelector('.tutor-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `tutor-message ${sender}`;
    messageDiv.innerHTML = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageDiv;
}

// Background Animation
function setupBackgroundAnimation() {
    const background = document.querySelector('.ai-background');
    if (!background) return;
    
    const neuralNetwork = document.createElement('div');
    neuralNetwork.className = 'neural-network';
    
    // Create neural nodes
    for (let i = 0; i < 5; i++) {
        const node = document.createElement('div');
        node.className = 'neural-node';
        neuralNetwork.appendChild(node);
    }
    
    background.appendChild(neuralNetwork);
    
    // Add grid overlay
    const grid = document.createElement('div');
    grid.className = 'grid-overlay';
    background.appendChild(grid);
}

// Login functionality
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showNotification('Please enter both username and password', 'error');
        return;
    }
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = '/home';
            }, 1000);
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Connection error. Please try again.', 'error');
    }
}

// Quiz functionality
let quizQuestions = [];
let userAnswers = [];

async function startQuiz() {
    try {
        const response = await fetch('/get_quiz_questions');
        quizQuestions = await response.json();
        userAnswers = new Array(quizQuestions.length).fill(null);
        displayQuiz();
    } catch (error) {
        showNotification('Error loading quiz. Please try again.', 'error');
    }
}

function displayQuiz() {
    const container = document.getElementById('quiz-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    quizQuestions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'quiz-question';
        
        const questionText = document.createElement('h3');
        questionText.textContent = `${index + 1}. ${q.question}`;
        questionText.style.marginBottom = '1rem';
        questionDiv.appendChild(questionText);
        
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'quiz-options';
        
        q.options.forEach((option, optIndex) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'quiz-option';
            optionDiv.textContent = option;
            optionDiv.onclick = () => selectAnswer(index, optIndex, optionDiv);
            optionsDiv.appendChild(optionDiv);
        });
        
        questionDiv.appendChild(optionsDiv);
        container.appendChild(questionDiv);
    });
    
    const submitBtn = document.createElement('button');
    submitBtn.className = 'btn btn-primary';
    submitBtn.textContent = 'Submit Quiz';
    submitBtn.style.marginTop = '2rem';
    submitBtn.onclick = submitQuiz;
    container.appendChild(submitBtn);
}

function selectAnswer(questionIndex, answerIndex, element) {
    // Remove previous selection
    const parent = element.parentElement;
    parent.querySelectorAll('.quiz-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    // Add new selection
    element.classList.add('selected');
    userAnswers[questionIndex] = answerIndex;
}

async function submitQuiz() {
    // Check if all questions are answered
    if (userAnswers.includes(null)) {
        showNotification('Please answer all questions before submitting', 'error');
        return;
    }
    
    try {
        const response = await fetch('/submit_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answers: userAnswers })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showQuizResults(data);
        } else {
            showNotification('Error submitting quiz. Please try again.', 'error');
        }
    } catch (error) {
        showNotification('Connection error. Please try again.', 'error');
    }
}

function showQuizResults(data) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    `;
    
    const resultsCard = document.createElement('div');
    resultsCard.className = 'card';
    resultsCard.style.cssText = `
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    `;
    
    const rec = data.recommendations;
    
    resultsCard.innerHTML = `
        <h2 class="card-title">Quiz Results</h2>
        <div style="text-align: center; margin: 2rem 0;">
            <div style="font-size: 4rem; color: var(--primary-gold);">${rec.percentage.toFixed(0)}%</div>
            <div style="font-size: 1.5rem; margin-top: 1rem;">
                Score: ${rec.score}/${rec.total}
            </div>
            <div class="badge badge-${rec.level.toLowerCase()}" style="margin-top: 1rem; font-size: 1rem;">
                ${rec.level_name} Level
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0;">
            <h3 style="color: var(--accent-blue); margin-bottom: 1rem;">AI Analysis</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">${rec.message}</p>
            <p><strong>Content Type:</strong> ${rec.content_type}</p>
        </div>
        
        <div style="margin: 1.5rem 0;">
            <h4 style="color: var(--primary-gold); margin-bottom: 1rem;">Focus Areas:</h4>
            <ul style="list-style: none; padding: 0;">
                ${rec.focus_areas.map(area => `
                    <li style="padding: 0.5rem; background: rgba(0,212,255,0.1); margin-bottom: 0.5rem; border-radius: 8px;">
                        ${area}
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div style="margin: 1.5rem 0;">
            <h4 style="color: var(--primary-gold); margin-bottom: 1rem;">Suggested Topics:</h4>
            <ul style="list-style: none; padding: 0;">
                ${rec.suggested_topics.map(topic => `
                    <li style="padding: 0.5rem; background: rgba(212,175,55,0.1); margin-bottom: 0.5rem; border-radius: 8px;">
                        ${topic}
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <button class="btn btn-primary" onclick="window.location.href='/ai_suggestions'">
                View Detailed Suggestions
            </button>
            <button class="btn btn-secondary" onclick="window.location.href='/learning_content'">
                Start Learning
            </button>
            <button class="btn btn-outline" onclick="this.parentElement.parentElement.parentElement.remove()">
                Close
            </button>
        </div>
    `;
    
    modal.appendChild(resultsCard);
    document.body.appendChild(modal);
}

// Profile update
async function updateProfile(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        education: document.getElementById('education').value,
        dob: document.getElementById('dob').value,
        mobile: document.getElementById('mobile').value
    };
    
    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Profile updated successfully!', 'success');
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Error updating profile. Please try again.', 'error');
    }
}

// Mark topic as complete
async function markTopicComplete(topicId) {
    try {
        const response = await fetch('/mark_complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic_id: topicId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Topic marked as complete!', 'success');
            
            // Update UI
            const checkbox = document.querySelector(`[data-topic="${topicId}"]`);
            if (checkbox) {
                checkbox.checked = true;
                checkbox.disabled = true;
            }
            
            // Reload page to update progress
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
    } catch (error) {
        showNotification('Error updating progress', 'error');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 30px;
        background: ${type === 'error' ? 'rgba(255, 51, 102, 0.95)' : 
                     type === 'success' ? 'rgba(0, 255, 136, 0.95)' : 
                     'rgba(0, 212, 255, 0.95)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 30px rgba(0, 0, 0, 0.5);
        z-index: 10000;
        font-family: var(--font-body);
        font-weight: 600;
        animation: slideInRight 0.4s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.4s ease';
        setTimeout(() => {
            notification.remove();
        }, 400);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// Update progress bar animations
function animateProgressBar(elementId, percentage) {
    const progressBar = document.getElementById(elementId);
    if (progressBar) {
        setTimeout(() => {
            progressBar.style.width = percentage + '%';
        }, 100);
    }
}

// Initialize progress bars on page load
window.addEventListener('load', function() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.getAttribute('data-progress');
        if (width) {
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width + '%';
            }, 100);
        }
    });
});
