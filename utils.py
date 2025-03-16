import numpy as np
import base64

def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender == "Male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def get_macro_split(goal):
    """Return macro nutrient split based on goal"""
    splits = {
        "Weight Loss": {"protein": 0.4, "carbs": 0.3, "fats": 0.3},
        "Muscle Gain": {"protein": 0.3, "carbs": 0.5, "fats": 0.2},
        "Maintenance": {"protein": 0.3, "carbs": 0.4, "fats": 0.3}
    }
    return splits[goal]

def get_workout_recommendation(goal, fitness_level):
    """Generate workout recommendations based on goal and fitness level"""
    workouts = {
        "Weight Loss": {
            "Beginner": [
                "30 minutes walking daily",
                "2x full body strength training",
                "1x yoga or stretching"
            ],
            "Intermediate": [
                "30 minutes jogging/cycling",
                "3x full body HIIT",
                "2x strength training"
            ],
            "Advanced": [
                "45 minutes high-intensity cardio",
                "4x split strength training",
                "2x HIIT sessions"
            ]
        },
        "Muscle Gain": {
            "Beginner": [
                "3x full body strength training",
                "2x light cardio",
                "Focus on compound exercises"
            ],
            "Intermediate": [
                "4x upper/lower split",
                "2x moderate cardio",
                "Progressive overload focus"
            ],
            "Advanced": [
                "5x body part split",
                "2x conditioning work",
                "Periodization training"
            ]
        },
        "Maintenance": {
            "Beginner": [
                "2x full body strength",
                "2x cardio sessions",
                "1x flexibility work"
            ],
            "Intermediate": [
                "3x strength training",
                "2x cardio sessions",
                "1x mobility work"
            ],
            "Advanced": [
                "4x strength training",
                "2x cardio sessions",
                "1x active recovery"
            ]
        }
    }
    return workouts[goal][fitness_level]

def get_default_profile_photo():
    """Generate default profile photo as base64 encoded data URI"""
    svg_string = """
    <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
        <rect width="150" height="150" fill="#f0f2f5"/>
        <circle cx="75" cy="60" r="30" fill="#90caf9"/>
        <path d="M75,100 C45,100 25,120 25,150 L125,150 C125,120 105,100 75,100" fill="#90caf9"/>
    </svg>
    """
    # Convert SVG to base64
    svg_bytes = svg_string.encode('utf-8')
    base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{base64_svg}"

def download_user_data():
    """This function has been moved to app.py as it requires Streamlit session state"""
    pass