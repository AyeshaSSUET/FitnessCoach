import streamlit as st
from groq import Groq
import re

api_key=st.secrets["fitness_api_key"]
# Function to generate a personalized fitness and meal plan using Groq API
def generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal):
    client = Groq(api_key=api_key)  # Initialize Groq client with the provided API key

    prompt = f"""
    I have the following user details:
    - Age: {age} years
    - Weight: {weight} kg
    - Height: {height} cm
    - Gender: {gender}
    - Diet Preferences: {diet_pref}
    - Fitness Goal: {fitness_goal}
    
    Based on this information, provide a customized fitness plan and a meal plan that aligns with the user's goals and dietary preferences.
    Include exercise video links if available.
    """

    # Send the prompt to Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
    )

    # Return the generated text as the plan
    return chat_completion.choices[0].message.content

# Function to extract and format video links from the text
def extract_video_links(text):
    # Regex pattern to match video URLs (You might need to adjust the pattern based on actual URL formats)
    video_url_pattern = re.compile(r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://(?:www\.)?vimeo\.com/\d+)')
    links = video_url_pattern.findall(text)
    
    # Replace URLs in the text with clickable links
    for url in links:
        text = text.replace(url, f'<a href="{url}" target="_blank">{url}</a>')
    
    return text

# Streamlit app
def main():
    # Apply custom styles
    st.markdown(
        """
        <style>
        /* Main Title Style */
        .main-title {
            font-size: 3em;
            color: #FF6347; /* Tomato color */
            text-align: center;
            margin-bottom: 0.5em;
        }

        /* Description Style */
        .description {
            font-size: 1.2em;
            color: #2E8B57; /* Sea Green color */
            text-align: center;
            margin-bottom: 2em;
        }

        /* Sidebar Background Color */
        .css-1d391kg { /* This class is for the sidebar */
            background-color: #2E8B57 !important; /* Sea Green background */
        }

        /* Sidebar Text Color */
        .css-1cpxqw2 { /* This class is for the sidebar text */
            color: #FFFFFF !important; /* White text */
        }

        /* Input Box Style */
        .css-1n76uvr, .css-7jyd01, .css-vfskoc, .css-1ktcvv5 { 
            color: #2E8B57 !important; /* Sea Green input text */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Fancy title and description
    st.markdown(
        """
        <div class="main-title">AI-Powered Fitness & Nutrition Coach</div>
        <div class="description">
           Welcome to the AI-Powered Fitness & Nutrition Coach, your personalized guide to achieving your fitness goals. This innovative application leverages advanced AI technology to deliver customized workout and meal plans tailored to your unique needs.
           

        </div>
        """, unsafe_allow_html=True
    )

    # Sidebar for user inputs
    st.sidebar.header("Enter Your Details")
    
    age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    diet_pref = st.sidebar.selectbox("Diet Preferences", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    fitness_goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "Endurance", "Flexibility"])

    # Collect the API key for Groq
    

    # Generate and display the fitness plan and meal options
    if st.sidebar.button("Generate Plan"):
        if api_key:
            fitness_and_meal_plan = generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal)
            formatted_plan = extract_video_links(fitness_and_meal_plan)
            st.subheader("Your Personalized Fitness Plan & Meal Options")
            st.markdown(formatted_plan, unsafe_allow_html=True)
        else:
            st.error("Please enter a valid Groq API key.")

if __name__ == "__main__":
    main()
