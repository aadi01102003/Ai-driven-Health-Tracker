import os
import json
from openai import OpenAI

def get_openai_client():
    """Get OpenAI client if API key is available"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def get_diet_recommendations(age, weight, height, gender, activity_level, goal, current_diet=None):
    """Get personalized diet recommendations using OpenAI"""
    client = get_openai_client()
    if not client:
        return {
            "error": "OpenAI API key not set. AI recommendations are not available.",
            "message": "Please set up your OpenAI API key to enable AI recommendations."
        }

    prompt = f"""
    As a nutrition expert, provide personalized diet recommendations for:
    - Age: {age}
    - Weight: {weight}kg
    - Height: {height}cm
    - Gender: {gender}
    - Activity Level: {activity_level}
    - Goal: {goal}

    Please provide a detailed response with:
    1. Daily meal plan with specific portions and timing
    2. Comprehensive list of recommended foods with nutritional benefits
    3. Foods to avoid and why
    4. Meal timing strategies for optimal results
    5. Supplement recommendations if needed
    6. Tips for meal prep and planning
    7. Strategies for dining out while staying on track
    8. Hydration recommendations

    Format the response as JSON with these keys:
    meal_plan, foods_to_include, foods_to_avoid, timing_tips, 
    supplements, meal_prep_tips, dining_out_tips, hydration
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return {
            "error": "Failed to get AI recommendations",
            "message": str(e)
        }

def get_workout_recommendations(age, fitness_level, goal, medical_conditions=None):
    """Get personalized workout recommendations using OpenAI"""
    client = get_openai_client()
    if not client:
        return {
            "error": "OpenAI API key not set. AI recommendations are not available.",
            "message": "Please set up your OpenAI API key to enable AI recommendations."
        }

    prompt = f"""
    As a fitness expert, provide detailed workout recommendations for:
    - Age: {age}
    - Fitness Level: {fitness_level}
    - Goal: {goal}
    - Medical Conditions: {medical_conditions or 'None'}

    Please provide a comprehensive plan including:
    1. Detailed weekly workout schedule
    2. Exercise details with sets, reps, intensity, and form cues
    3. Progression plan for 8 weeks
    4. Recovery and mobility work
    5. Warm-up and cool-down routines
    6. Progress tracking metrics
    7. Alternative exercises for each movement
    8. Tips for injury prevention
    9. Recommended rest periods
    10. Cardio integration strategies

    Format the response as JSON with these keys:
    weekly_schedule, exercise_details, progression_plan, recovery_tips,
    warmup_cooldown, tracking_metrics, alternative_exercises,
    injury_prevention, rest_guidelines, cardio_integration
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return {
            "error": "Failed to get AI recommendations",
            "message": str(e)
        }

def get_personalized_diet_plan(profile, dietary_preferences):
    """Get highly personalized diet recommendations using OpenAI"""
    client = get_openai_client()
    if not client:
        return {
            "error": "OpenAI API key not set. AI recommendations are not available.",
            "message": "Please set up your OpenAI API key to enable AI recommendations."
        }

    prompt = f"""
    As a nutrition expert, create a highly personalized diet plan for someone with these characteristics:
    - Age: {profile['age']}
    - Weight: {profile['weight']}kg
    - Height: {profile['height']}cm
    - Gender: {profile['gender']}
    - Activity Level: {profile['activity_level']}
    - Fitness Goal: {profile['goal']}

    Dietary Preferences and Restrictions:
    - Allergies: {dietary_preferences.get('allergies', [])}
    - Dietary Restrictions: {dietary_preferences.get('restrictions', [])}
    - Preferred Cuisines: {dietary_preferences.get('preferred_cuisines', [])}
    - Disliked Ingredients: {dietary_preferences.get('disliked_ingredients', [])}
    - Meal Timing Preferences: {dietary_preferences.get('meal_timing_preferences', {})}

    Please provide a comprehensive nutrition plan including:
    1. Detailed weekly meal plan with exact portions and macronutrient breakdowns
    2. Shopping list organized by food categories
    3. Meal prep instructions and timeline
    4. Alternative meal suggestions for variety
    5. Restaurant ordering guide based on preferred cuisines
    6. Supplement recommendations with timing
    7. Hydration schedule
    8. Tips for special occasions and social events
    9. Progress tracking metrics
    10. Common mistakes to avoid

    Format the response as JSON with these keys:
    weekly_meal_plan, shopping_list, meal_prep_guide, alternatives,
    restaurant_guide, supplements, hydration_schedule, special_occasions,
    tracking_metrics, common_mistakes
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return {
            "error": "Failed to get personalized diet plan",
            "message": str(e)
        }