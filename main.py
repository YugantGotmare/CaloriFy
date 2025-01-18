from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import sqlite3
from io import BytesIO

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database setup
def init_db():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_time TEXT,
            calorie_report TEXT,
            image BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_history(meal_time, calorie_report, image):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (meal_time, calorie_report, image) VALUES (?, ?, ?)",
              (meal_time, calorie_report, image))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# Function to generate response
def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to process uploaded image
def input_image_setup(uploaded_file):
    try:
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

# Page Configuration
st.set_page_config(page_title="The Nutritionist", layout="wide")

# Initialize Database
init_db()

# Header
st.title("🍎 The Nutritionist")
st.write("Upload an image of your meal, and we'll estimate the calories, provide dietary advice, and more!")

# Sidebar for User Settings
with st.sidebar:
    st.header("Settings")
    meal_time = st.selectbox("Select Meal Time", ["Breakfast", "Lunch", "Dinner", "Snack"])
    portion_size = st.radio("Select Portion Size", ["Small", "Medium", "Large"], index=1)

# File Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display Uploaded Image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Generate Button
submit = st.button("Analyze My Meal")

# Prompt
input_prompt = f"""
You are an expert nutritionist. Analyze the food items in the image and provide:
1. Calorie content for each item based on a {portion_size} portion.
2. A total calorie count.
3. Macronutrient breakdown (carbs, protein, fats).
4. Whether the meal is healthy, balanced, or unhealthy.
5. Suggestions for making the meal healthier.

Format the response as:
1. Item 1 - no. of calories
2. Item 2 - no. of calories
---
Total: XX calories
Macronutrients: Carbs - Xg, Protein - Yg, Fats - Zg
Health Status: Healthy/Balanced/Unhealthy
Suggestions: ...
"""

# Analyze Meal
if submit:
    st.info("Analyzing the image... Please wait.")
    image_data = input_image_setup(uploaded_file)
    if image_data:
        response = get_gemini_response(input_prompt, image_data)
        st.success("Analysis Complete!")
        st.subheader("Results:")
        st.write(response)

        # Save to History
        with BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_blob = buffer.getvalue()
        save_to_history(meal_time, response, image_blob)

        # Download Button
        st.download_button(
            label="Download Results as Text",
            data=response,
            file_name="calorie_report.txt",
            mime="text/plain"
        )

# View History
st.header("📜 Analysis History")
history = get_history()
if history:
    for entry in history:
        st.subheader(f"Meal Time: {entry[1]} | Date: {entry[4]}")
        st.write(entry[2])
else:
    st.write("No history available.")
