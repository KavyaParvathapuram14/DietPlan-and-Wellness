import streamlit as st
import pandas as pd
import random

# Load the dataset with the updated caching method
@st.cache_data
def load_data():
    return pd.read_csv('All_Diets.csv')

data = load_data()

# App Title with Colors
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Diet Plan Generator & Wellness Tracker</h1>", unsafe_allow_html=True)

# Sidebar Styling
st.sidebar.markdown("<h2 style='color: #2196F3;'>Personalize Your Plan</h2>", unsafe_allow_html=True)

# Section 1: User Diet Preferences
st.sidebar.header("Diet Preferences")
diet_type = st.sidebar.radio("Select a diet type:", data['Diet_type'].unique())
calorie_target = st.sidebar.slider("Calorie target per day (kcal):", 1000, 3000, 2000, step=100)
protein_ratio = st.sidebar.slider("Protein (%)", 10, 50, 30)
carbs_ratio = st.sidebar.slider("Carbs (%)", 10, 70, 40)
fat_ratio = 100 - protein_ratio - carbs_ratio

st.sidebar.markdown(f"**Fat (%)**: {fat_ratio}")

# Filter data based on user inputs
filtered_data = data[data['Diet_type'] == diet_type]

# Generate Diet Plan
def generate_diet_plan(filtered_data, calorie_target, protein_ratio, carbs_ratio, fat_ratio):
    meal_plan = []
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_calories = 0

    while total_calories < calorie_target:
        meal = filtered_data.sample(1).iloc[0]
        meal_plan.append(meal['Recipe_name'])
        total_protein += meal['Protein(g)']
        total_carbs += meal['Carbs(g)']
        total_fat += meal['Fat(g)']
        total_calories = 4 * (total_protein + total_carbs) + 9 * total_fat

    return meal_plan, total_protein, total_carbs, total_fat, total_calories

diet_plan, protein, carbs, fat, calories = generate_diet_plan(filtered_data, calorie_target, protein_ratio, carbs_ratio, fat_ratio)

# Display Diet Plan
st.markdown("<h2 style='color: #FF5722;'>Your Daily Diet Plan</h2>", unsafe_allow_html=True)
for i, meal in enumerate(diet_plan, 1):
    st.markdown(f"<h4 style='color: #673AB7;'>{i}. {meal}</h4>", unsafe_allow_html=True)

# Nutritional Summary with Metrics
st.markdown("<h2 style='color: #FFC107;'>Nutritional Summary</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Protein (g)", f"{protein:.2f}")
col2.metric("Carbs (g)", f"{carbs:.2f}")
col3.metric("Fat (g)", f"{fat:.2f}")
col4.metric("Calories (kcal)", f"{calories:.2f}")

# Section 2: Employee Wellness and Stress Levels
st.markdown("<h2 style='color: #009688;'>Employee Wellness</h2>", unsafe_allow_html=True)
stress_level = st.slider("Rate your stress level (1 - Low, 10 - High):", 1, 10, 5)
sleep_hours = st.number_input("Average sleep hours per night:", min_value=0.0, max_value=24.0, value=7.0)
exercise_minutes = st.number_input("Exercise minutes per day:", min_value=0, max_value=300, value=30)

# Progress Bars for Visual Appeal
st.markdown("<h3 style='color: #795548;'>Wellness Summary</h3>", unsafe_allow_html=True)
st.progress(stress_level * 10)
st.caption("Stress Level Progress")

if stress_level >= 7:
    st.info("Consider stress-relief activities such as meditation, yoga, or deep breathing exercises.")
elif 4 <= stress_level < 7:
    st.success("You seem to be managing your stress well. Keep up with regular exercise and healthy habits!")
else:
    st.success("Your stress level is low. Maintain a balanced lifestyle to keep it that way.")

if sleep_hours < 6:
    st.warning("It looks like you're not getting enough sleep. Aim for at least 7-8 hours of quality sleep each night.")
else:
    st.success("Your sleep habits seem healthy. Keep prioritizing rest!")

if exercise_minutes < 30:
    st.warning("Try to increase your physical activity to at least 30 minutes a day for better stress management.")
else:
    st.success("Great job staying active! Regular exercise helps with both physical and mental wellness.")

# Section 3: AI Assistant
st.markdown("<h2 style='color: #E91E63;'>AI Assistant</h2>", unsafe_allow_html=True)
user_query = st.text_input("Ask me anything about your diet, recipes, or wellness:")
if user_query:
    st.markdown(f"<h4 style='color: #3F51B5;'>AI Response: Here's some advice or insights regarding your query...</h4>", unsafe_allow_html=True)
