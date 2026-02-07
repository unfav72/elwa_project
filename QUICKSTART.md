# ELWA - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd elwa_project
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 First Login

1. **Create Account:**
   - Enter any username (e.g., "student1")
   - Enter any password (e.g., "password")
   - Click "Login / Register"

2. **Take the Quiz:**
   - From the homepage, click "Take Assessment Quiz"
   - Click "Start Quiz"
   - Answer 10 randomized questions
   - Submit to get AI recommendations

3. **Explore Features:**
   - View AI Suggestions
   - Browse Learning Content
   - Update Your Profile
   - Track Progress in "My Learning"
   - Check Leaderboard

## 💡 Tips for Best Experience

- **Take the quiz first** to get personalized AI recommendations
- **Mark topics as complete** as you learn them
- **Use the AI Tutor** (bottom-right corner) for quick help
- **Maintain streaks** by learning daily
- **Compete** on the leaderboard for motivation

## 🎨 Main Features

✅ AI-powered quiz analysis  
✅ Personalized learning recommendations  
✅ Comprehensive Python content (basics to ML/AI/Blockchain)  
✅ Progress tracking with streaks  
✅ Global leaderboard  
✅ AI Tutor chatbot on every page  
✅ Beautiful futuristic UI with animations  

## 🔧 Troubleshooting

**Problem:** Port 5000 already in use  
**Solution:** Change port in app.py (last line):
```python
app.run(debug=True, port=5001)  # Use different port
```

**Problem:** Module not found  
**Solution:** Install Flask:
```bash
pip install Flask
```

**Problem:** Logo not showing  
**Solution:** Make sure logo.jpg is in static/images/ folder

## 📱 Navigation

- **Menu** (top-left): Access all pages
- **Logo** (top-center): Always visible
- **AI Tutor** (bottom-right): Click 🤖 icon

## 🎓 Learning Path

1. Take quiz → Get level assessment
2. View AI suggestions → See personalized recommendations
3. Browse content → Find topics to learn
4. Complete topics → Mark as done
5. Retake quiz → Track improvement
6. Climb leaderboard → Compete with others

Enjoy your Python learning journey with ELWA! 🚀
