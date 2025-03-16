import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
from datetime import datetime
from utils import (
    calculate_bmr, calculate_tdee, get_macro_split,
    get_workout_recommendation, get_default_profile_photo, download_user_data
)
from data_manager import DataManager
from ai_recommendations import get_diet_recommendations, get_workout_recommendations, get_personalized_diet_plan

# Initialize session state
try:
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
except Exception as e:
    st.error(f"Failed to connect to database: {str(e)}")
    st.stop()

if 'profile' not in st.session_state:
    st.session_state.profile = {}
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

def set_mobile_responsive_config():
    st.set_page_config(
        page_title="Health & Fitness Tracker",
        layout="wide",
        initial_sidebar_state="collapsed"  # Better for mobile
    )

def main():
    set_mobile_responsive_config()
    st.title("Health & Fitness Tracker")

    # Make navigation more touch-friendly for mobile
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "",
        ["Profile", "Food Tracking", "AI Recommendations", "Workout Plan", "Progress"],
        label_visibility="collapsed",
        key="nav"  # Add key to prevent duplicates
    )

    # Add CSS to make buttons more touch-friendly
    st.markdown("""
        <style>
        .stButton>button {
            min-height: 48px;  /* Minimum touch target size */
            margin: 8px 0;     /* Add spacing between buttons */
        }
        .stSelectbox select {
            min-height: 48px;  /* Make dropdowns touch-friendly */
        }
        /* Make forms more readable on mobile */
        .stForm {
            padding: 1rem;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
        }
        /* Improve readability of metrics on mobile */
        .stMetric {
            font-size: 1.2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if page == "Profile":
        show_profile_page()
    elif page == "Food Tracking":
        show_food_tracking_page()
    elif page == "AI Recommendations":
        show_ai_recommendations_page()
    elif page == "Workout Plan":
        show_workout_page()
    elif page == "Progress":
        show_progress_page()

def show_profile_page():
    st.header("Profile Settings")

    # Display profile photo with default if none exists
    col1, col2 = st.columns([1, 3])
    with col1:
        if 'photo' in st.session_state.profile:
            st.image(st.session_state.profile['photo'], width=150)
        else:
            st.image(get_default_profile_photo(), width=150)

        # Add photo upload button
        photo = st.file_uploader("Update Photo", type=['jpg', 'jpeg', 'png'], key="profile_photo")
        if photo:
            st.session_state.profile['photo'] = photo
            st.rerun()

    with col2:
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", value=st.session_state.profile.get('first_name', ''))
                height = st.number_input("Height (cm)", 100, 250, value=st.session_state.profile.get('height', 170))
                gender = st.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.profile.get('gender') == "Male" else 1)
                activity_level = st.selectbox(
                    "Activity Level",
                    ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
                    index=0
                )
                goal = st.selectbox(
                    "Goal",
                    ["Weight Loss", "Muscle Gain", "Maintenance"],
                    index=0
                )

            with col2:
                last_name = st.text_input("Last Name", value=st.session_state.profile.get('last_name', ''))
                weight = st.number_input("Weight (kg)", 30, 300, value=st.session_state.profile.get('weight', 70))
                ethnicity = st.text_input("Ethnicity", value=st.session_state.profile.get('ethnicity', ''))
                age = st.number_input("Age", 15, 100, value=st.session_state.profile.get('age', 30))
                fitness_level = st.selectbox(
                    "Fitness Level",
                    ["Beginner", "Intermediate", "Advanced"],
                    index=0
                )

            medical_conditions = st.text_area("Medical Conditions (if any)", value=st.session_state.profile.get('medical_conditions', ''))

            if st.form_submit_button("Save Profile"):
                st.session_state.profile.update({
                    'first_name': first_name,
                    'last_name': last_name,
                    'ethnicity': ethnicity,
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'gender': gender,
                    'activity_level': activity_level,
                    'fitness_level': fitness_level,
                    'goal': goal,
                    'medical_conditions': medical_conditions
                })
                st.success("Profile updated successfully!")

                # Calculate and display daily targets
                bmr = calculate_bmr(weight, height, age, gender)
                tdee = calculate_tdee(bmr, activity_level)
                macro_split = get_macro_split(goal)

                st.subheader("Your Daily Targets:")
                st.write(f"Daily Calories: {int(tdee)} kcal")
                st.write(f"Protein: {int(tdee * macro_split['protein'] / 4)}g")
                st.write(f"Carbs: {int(tdee * macro_split['carbs'] / 4)}g")
                st.write(f"Fats: {int(tdee * macro_split['fats'] / 9)}g")

    # Add dietary preferences section
    st.markdown("---")
    show_diet_preferences_section()
    st.markdown("---")
    st.subheader("Download Your Data")
    if st.button("Export Fitness Data"):
        data = download_user_data()
        if data:
            st.download_button(
                label="Download JSON",
                data=data,
                file_name="fitness_data.json",
                mime="application/json"
            )
            st.info("Your data has been prepared for download. Click the button above to save it.")


def show_food_tracking_page():
    st.header("Food Tracking")

    try:
        # Display daily totals
        daily_totals = st.session_state.data_manager.get_daily_totals()
        st.subheader("Today's Totals")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories", f"{int(daily_totals['calories'])} kcal")
        c2.metric("Protein", f"{int(daily_totals['protein'])}g")
        c3.metric("Carbs", f"{int(daily_totals['carbs'])}g")
        c4.metric("Fats", f"{int(daily_totals['fats'])}g")

        # Add/Edit food form
        st.subheader("Add Food" if st.session_state.edit_index is None else "Edit Food")
        with st.form("food_entry"):
            food = st.text_input("Food Item")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                calories = st.number_input("Calories", 0, 2000)
            with col2:
                protein = st.number_input("Protein (g)", 0, 200)
            with col3:
                carbs = st.number_input("Carbs (g)", 0, 200)
            with col4:
                fats = st.number_input("Fats (g)", 0, 200)

            if st.form_submit_button("Save"):
                if st.session_state.edit_index is not None:
                    st.session_state.data_manager.update_food_entry(
                        st.session_state.edit_index,
                        food, calories, protein, carbs, fats
                    )
                    st.session_state.edit_index = None
                    st.success("Food entry updated successfully!")
                else:
                    st.session_state.data_manager.add_food_entry(
                        food, calories, protein, carbs, fats
                    )
                    st.success("Food entry added successfully!")
                st.rerun()

        # Create larger pie chart for macros
        if sum([daily_totals['protein'], daily_totals['carbs'], daily_totals['fats']]) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Protein', 'Carbs', 'Fats'],
                values=[daily_totals['protein'] * 4, daily_totals['carbs'] * 4, daily_totals['fats'] * 9],
                hole=.3
            )])
            fig.update_layout(
                title="Macro Distribution",
                height=500,  # Increased height
                width=800,   # Set specific width
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,  # Move legend below chart
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=60, b=100)  # Adjust margins
            )
            st.plotly_chart(fig, use_container_width=True)

        # Food log table
        st.subheader("Today's Food Log")
        today_log = st.session_state.data_manager.get_todays_food_log()

        for entry in today_log:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
            with col1:
                st.write(entry['food'])
            with col2:
                st.write(f"{entry['calories']} kcal")
            with col3:
                st.write(f"{entry['protein']}g protein")
            with col4:
                st.write(f"{entry['carbs']}g carbs")
            with col5:
                st.write(f"{entry['fats']}g fats")
            with col6:
                if st.button("Edit", key=f"edit_{entry['id']}"):
                    st.session_state.edit_index = entry['id']
                    st.rerun()

        # AI Diet Recommendations
        if st.session_state.profile:
            st.subheader("AI Diet Recommendations")
            if st.button("Get AI Diet Suggestions"):
                with st.spinner("Generating personalized diet recommendations..."):
                    recommendations = get_diet_recommendations(
                        st.session_state.profile['age'],
                        st.session_state.profile['weight'],
                        st.session_state.profile['height'],
                        st.session_state.profile['gender'],
                        st.session_state.profile['activity_level'],
                        st.session_state.profile['goal']
                    )
                    show_diet_recommendations(recommendations)

    except Exception as e:
        st.error(f"Error accessing food tracking data: {str(e)}")

    # Add advanced diet recommendations section
    st.markdown("---")
    show_advanced_diet_recommendations()


def show_workout_page():
    st.header("Workout Recommendations")

    if not st.session_state.profile:
        st.warning("Please complete your profile first!")
        return

    # AI Workout Recommendations
    st.subheader("AI Workout Plan")
    if st.button("Get AI Workout Suggestions"):
        with st.spinner("Generating personalized workout recommendations..."):
            recommendations = get_workout_recommendations(
                st.session_state.profile['age'],
                st.session_state.profile['fitness_level'],
                st.session_state.profile['goal'],
                st.session_state.profile.get('medical_conditions')
            )
            show_workout_recommendations(recommendations)

    # Basic workout suggestions
    st.subheader("Basic Workout Plan")
    workouts = get_workout_recommendation(
        st.session_state.profile['goal'],
        st.session_state.profile['fitness_level']
    )

    # Display workout schedule
    days = ["Monday", "Wednesday", "Friday"] if st.session_state.profile['fitness_level'] == "Beginner" else \
           ["Monday", "Tuesday", "Thursday", "Friday", "Saturday"]

    for day, workout in zip(days, workouts):
        with st.expander(f"{day}'s Workout"):
            st.write(workout)

            # Add exercise details based on the workout type
            if "strength training" in workout.lower():
                st.markdown("""
                **Recommended exercises:**
                - Squats: 3 sets x 8-12 reps
                - Push-ups/Bench Press: 3 sets x 8-12 reps
                - Rows: 3 sets x 8-12 reps
                - Core exercises: 3 sets x 15-20 reps

                **Rest between sets:** 60-90 seconds
                """)
            elif "cardio" in workout.lower():
                st.markdown("""
                **Intensity guide:**
                - Warm-up: 5 minutes at low intensity
                - Main session: Alternate between:
                  - 2 minutes moderate pace
                  - 1 minute high intensity
                - Cool-down: 5 minutes easy pace
                """)

    # Additional tips
    st.subheader("Training Tips")
    st.info("""
    - Stay hydrated: Drink water before, during, and after workouts
    - Warm-up: 5-10 minutes of light cardio before each session
    - Form: Focus on proper form over weight/intensity
    - Rest: Allow 24-48 hours between training the same muscle groups
    """)


def show_progress_page():
    st.header("Progress Tracking")

    try:
        # Weight tracking
        with st.form("weight_entry"):
            weight = st.number_input("Current Weight (kg)", 30.0, 300.0)
            if st.form_submit_button("Log Weight"):
                st.session_state.data_manager.add_weight_entry(weight)
                st.success("Weight logged successfully!")

        # Weight progress chart
        weight_history = st.session_state.data_manager.get_weight_history()
        if weight_history:
            df = pd.DataFrame(weight_history)
            fig = px.line(
                df,
                x='date',
                y='weight',
                title='Weight Progress'
            )
            st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error accessing progress tracking data: {str(e)}")


def show_diet_recommendations(recommendations):
    """Display enhanced diet recommendations"""
    if isinstance(recommendations, str):
        recommendations = json.loads(recommendations)

    if 'error' not in recommendations:
        with st.expander("📋 Meal Plan", expanded=True):
            st.write(recommendations['meal_plan'])
        with st.expander("🥗 Recommended Foods"):
            st.write(recommendations['foods_to_include'])
        with st.expander("⛔ Foods to Avoid"):
            st.write(recommendations['foods_to_avoid'])
        with st.expander("⏰ Meal Timing"):
            st.write(recommendations['timing_tips'])
        with st.expander("💊 Supplement Recommendations"):
            st.write(recommendations.get('supplements', 'No specific supplements recommended'))
        with st.expander("🔪 Meal Prep Tips"):
            st.write(recommendations.get('meal_prep_tips', 'No specific meal prep tips provided'))
        with st.expander("🍽️ Dining Out Guide"):
            st.write(recommendations.get('dining_out_tips', 'No specific dining out tips provided'))
        with st.expander("💧 Hydration Guide"):
            st.write(recommendations.get('hydration', 'No specific hydration recommendations provided'))
    else:
        st.error(recommendations['message'])


def show_workout_recommendations(recommendations):
    """Display enhanced workout recommendations"""
    if isinstance(recommendations, str):
        recommendations = json.loads(recommendations)

    if 'error' not in recommendations:
        with st.expander("📅 Weekly Schedule", expanded=True):
            st.write(recommendations['weekly_schedule'])
        with st.expander("💪 Exercise Details"):
            st.write(recommendations['exercise_details'])
        with st.expander("📈 8-Week Progression"):
            st.write(recommendations.get('progression_plan', 'No progression plan provided'))
        with st.expander("🧘‍♂️ Recovery & Mobility"):
            st.write(recommendations['recovery_tips'])
        with st.expander("🔥 Warm-up & Cool-down"):
            st.write(recommendations.get('warmup_cooldown', 'No warm-up/cool-down routine provided'))
        with st.expander("📊 Progress Tracking"):
            st.write(recommendations.get('tracking_metrics', 'No tracking metrics provided'))
        with st.expander("🔄 Alternative Exercises"):
            st.write(recommendations.get('alternative_exercises', 'No alternative exercises provided'))
        with st.expander("🏥 Injury Prevention"):
            st.write(recommendations.get('injury_prevention', 'No injury prevention tips provided'))
        with st.expander("⏱️ Rest Guidelines"):
            st.write(recommendations.get('rest_guidelines', 'No rest guidelines provided'))
        with st.expander("🏃‍♂️ Cardio Integration"):
            st.write(recommendations.get('cardio_integration', 'No cardio integration plan provided'))
    else:
        st.error(recommendations['message'])



def show_diet_preferences_section():
    """Show and manage dietary preferences"""
    st.subheader("Dietary Preferences")

    # Get current preferences
    current_prefs = st.session_state.data_manager.get_dietary_preferences()

    with st.form("dietary_preferences"):
        # Allergies
        allergies = st.multiselect(
            "Food Allergies",
            ["Dairy", "Eggs", "Tree Nuts", "Peanuts", "Shellfish", "Wheat", "Soy", "Fish"],
            default=current_prefs.get('allergies', [])
        )

        # Dietary Restrictions
        restrictions = st.multiselect(
            "Dietary Restrictions",
            ["Vegetarian", "Vegan", "Gluten-Free", "Kosher", "Halal", "Keto", "Low-Carb", "Paleo"],
            default=current_prefs.get('restrictions', [])
        )

        # Preferred Cuisines
        cuisines = st.multiselect(
            "Preferred Cuisines",
            ["Italian", "Mexican", "Chinese", "Japanese", "Indian", "Mediterranean", "American", "Thai"],
            default=current_prefs.get('preferred_cuisines', [])
        )

        # Disliked Ingredients
        disliked = st.text_area(
            "Disliked Ingredients (one per line)",
            value="\n".join(current_prefs.get('disliked_ingredients', []))
        )

        # Meal Timing Preferences
        st.subheader("Meal Timing Preferences")
        col1, col2 = st.columns(2)
        with col1:
            breakfast_time = st.time_input(
                "Preferred Breakfast Time",
                value=datetime.strptime(
                    current_prefs.get('meal_timing_preferences', {}).get('breakfast', '08:00'),
                    '%H:%M'
                ).time()
            )
            lunch_time = st.time_input(
                "Preferred Lunch Time",
                value=datetime.strptime(
                    current_prefs.get('meal_timing_preferences', {}).get('lunch', '13:00'),
                    '%H:%M'
                ).time()
            )
        with col2:
            dinner_time = st.time_input(
                "Preferred Dinner Time",
                value=datetime.strptime(
                    current_prefs.get('meal_timing_preferences', {}).get('dinner', '19:00'),
                    '%H:%M'
                ).time()
            )
            snacks_count = st.number_input(
                "Number of Snacks per Day",
                0, 5,
                value=current_prefs.get('meal_timing_preferences', {}).get('snacks_count', 2)
            )

        if st.form_submit_button("Save Preferences"):
            preferences = {
                'allergies': allergies,
                'restrictions': restrictions,
                'preferred_cuisines': cuisines,
                'disliked_ingredients': [x.strip() for x in disliked.split('\n') if x.strip()],
                'meal_timing_preferences': {
                    'breakfast': breakfast_time.strftime('%H:%M'),
                    'lunch': lunch_time.strftime('%H:%M'),
                    'dinner': dinner_time.strftime('%H:%M'),
                    'snacks_count': snacks_count
                }
            }
            st.session_state.data_manager.save_dietary_preferences(preferences)
            st.success("Dietary preferences saved successfully!")


def show_advanced_diet_recommendations():
    """Display advanced AI-powered diet recommendations"""
    st.subheader("Advanced Diet Recommendations")

    if not st.session_state.profile:
        st.warning("Please complete your profile first!")
        return

    dietary_prefs = st.session_state.data_manager.get_dietary_preferences()
    if not dietary_prefs:
        st.warning("Please set your dietary preferences first!")
        st.markdown("[Go to Dietary Preferences](#dietary-preferences)")
        return

    if st.button("Generate Personalized Diet Plan"):
        with st.spinner("Generating your personalized diet plan..."):
            recommendations = get_personalized_diet_plan(
                st.session_state.profile,
                dietary_prefs
            )

            if isinstance(recommendations, str):
                recommendations = json.loads(recommendations)

            if 'error' not in recommendations:
                with st.expander("📅 Weekly Meal Plan", expanded=True):
                    st.write(recommendations['weekly_meal_plan'])

                with st.expander("🛒 Shopping List"):
                    st.write(recommendations['shopping_list'])

                with st.expander("👩‍🍳 Meal Prep Guide"):
                    st.write(recommendations['meal_prep_guide'])

                with st.expander("🔄 Alternative Meals"):
                    st.write(recommendations['alternatives'])

                with st.expander("🍽️ Restaurant Guide"):
                    st.write(recommendations['restaurant_guide'])

                with st.expander("💊 Supplement Guide"):
                    st.write(recommendations['supplements'])

                with st.expander("💧 Hydration Schedule"):
                    st.write(recommendations['hydration_schedule'])

                with st.expander("🎉 Special Occasions"):
                    st.write(recommendations['special_occasions'])

                with st.expander("📊 Progress Tracking"):
                    st.write(recommendations['tracking_metrics'])

                with st.expander("⚠️ Common Mistakes"):
                    st.write(recommendations['common_mistakes'])
            else:
                st.error(recommendations['message'])


def download_user_data():
    """Create downloadable files for user data"""
    try:
        # Get user data
        profile = st.session_state.profile
        dietary_prefs = st.session_state.data_manager.get_dietary_preferences()
        weight_history = st.session_state.data_manager.get_weight_history()
        food_log = st.session_state.data_manager.get_todays_food_log()

        # Create a dictionary with all user data
        user_data = {
            "profile": profile,
            "dietary_preferences": dietary_prefs,
            "weight_history": weight_history,
            "food_log": food_log
        }

        # Convert to JSON string
        json_str = json.dumps(user_data, indent=2, default=str)

        return json_str
    except Exception as e:
        st.error(f"Error preparing download data: {str(e)}")
        return None

def show_ai_recommendations_page():
    """Display all AI-powered features in one place"""
    st.header("AI-Powered Recommendations")

    if not st.session_state.profile:
        st.warning("Please complete your profile first to get personalized recommendations!")
        return

    # Create tabs for different AI features
    diet_tab, workout_tab = st.tabs(["🍽️ Diet Recommendations", "💪 Workout Recommendations"])

    with diet_tab:
        st.subheader("Personalized Diet Plan")
        if st.button("Generate Diet Recommendations", key="diet_ai"):
            with st.spinner("Analyzing your profile and generating personalized diet recommendations..."):
                recommendations = get_diet_recommendations(
                    st.session_state.profile['age'],
                    st.session_state.profile['weight'],
                    st.session_state.profile['height'],
                    st.session_state.profile['gender'],
                    st.session_state.profile['activity_level'],
                    st.session_state.profile['goal']
                )
                show_diet_recommendations(recommendations)

        st.markdown("---")
        show_advanced_diet_recommendations()

    with workout_tab:
        st.subheader("Personalized Workout Plan")
        if st.button("Generate Workout Recommendations", key="workout_ai"):
            with st.spinner("Creating your personalized workout plan..."):
                recommendations = get_workout_recommendations(
                    st.session_state.profile['age'],
                    st.session_state.profile['fitness_level'],
                    st.session_state.profile['goal'],
                    st.session_state.profile.get('medical_conditions')
                )
                show_workout_recommendations(recommendations)

if __name__ == "__main__":
    main()