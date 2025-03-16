# 🧠 AI-Driven Health Tracker App

Welcome to the **AI-Driven Health Tracker App** — your smart companion to lead a healthier lifestyle. This app uses artificial intelligence to provide personalized diet and workout recommendations, track food intake, monitor weight progress, and more — all in one sleek and intuitive platform.

---

## 📱 Features

### 👤 Profile Section
- Add personal details: age, gender, height, weight, fitness goals, dietary preferences.
- Automatically calculates BMI and BMR.
- Personalized user dashboard.

### 🥗 Food Tracker
- Log daily meals and snacks.
- Search from a nutrition database or scan food items.
- Track calories, macronutrients, and micronutrients.
- Real-time daily intake summary.

### 🤖 AI-Powered Diet & Workout Recommendation
- Customized meal plans based on your health profile, goals, and preferences.
- AI-recommended workouts based on fitness level and available equipment.
- Adaptive recommendations as your data evolves.

### 📈 Progress Tracker
- Monitor your weight changes over time.
- Graphical visualizations of health metrics.
- Weekly and monthly summaries.

---

## 🖼️ Screenshots

| Home Dashboard | Food Tracker | AI Diet Plan | Workout Suggestions |
|----------------|--------------|----------------|---------------------|
| ![Home](screenshots/home.png) | ![Food Tracker](screenshots/food-tracker.png) | ![Diet](screenshots/ai-diet.png) | ![Workout](screenshots/workout.png) |

| Profile Page | Progress Tracker |
|--------------|------------------|
| ![Profile](screenshots/profile.png) | ![Progress](screenshots/progress-tracker.png) |

---

## 🛠️ Tech Stack

- **Frontend:** React Native / Flutter (cross-platform mobile)
- **Backend:** Node.js / Django REST API
- **Database:** PostgreSQL / MongoDB
- **AI Models:** Python (TensorFlow, Scikit-learn, GPT APIs for recommendations)
- **Authentication:** Firebase Auth / OAuth 2.0

---

## 🚀 Getting Started

### Prerequisites:
- Node.js / Python
- Mobile Emulator / Device
- API keys for Nutrition & Fitness APIs (e.g., Nutritionix, OpenAI, etc.)

### Setup Instructions:

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-health-tracker.git
cd ai-health-tracker

# Install dependencies
npm install         # For frontend
pip install -r requirements.txt  # For backend AI engine

# Start backend server
python backend/app.py

# Start frontend
npm start
