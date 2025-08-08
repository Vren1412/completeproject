import streamlit as st
from PIL import Image
import random

# ------------------------ 1. Title ------------------------
st.title(" Real-Time Movie Recommendation Engine")

# ------------------------ 2. Header and Subheader ------------------------
st.header("Welcome to CineMatch!")
st.subheader("Discover movies you'll love in real-time.")

# ------------------------ 3. Text ------------------------
st.text("This app suggests movies based on your preferences instantly.")

# ------------------------ 4. Markdown ------------------------
st.markdown("""
###  Features:
- Personalized Recommendations
- Real-time Filters
- Interactive Preferences
""")

# ------------------------ 5. Status Messages ------------------------
st.success(" Model Loaded Successfully!")
st.info("ℹ You can select your favorite genres and mood to get recommendations.")
st.warning(" Avoid selecting conflicting moods for better results.")
st.error(" Invalid selection detected in past run.")  # Example placeholder
try:
    # Simulate a handled exception
    1 / 1
except Exception as e:
    st.exception(e)

# ------------------------ 6. Write ------------------------
st.write("## 🎥 Let's Build Your Movie Profile")
st.write("Tell us what you're in the mood for today...")

# ------------------------ 7. Display Images ------------------------
img = Image.open("movie_banner.jpg")  # Replace with a real image path
st.image(img, caption="Tonight’s Movie Mood", use_column_width=True)

# ------------------------ 8. Checkbox ------------------------
kids_friendly = st.checkbox("👶 Show only Kids Friendly movies")

# ------------------------ 9. Radio Button ------------------------
mood = st.radio(
    "What's your current mood?",
    ('Happy', 'Sad', 'Excited', 'Romantic', 'Adventurous')
)

# ------------------------ 10. Selection Box ------------------------
genre = st.selectbox(
    "Select your favorite genre",
    ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Documentary']
)

# ------------------------ 11. Multi-Selectbox ------------------------
actors = st.multiselect(
    "Pick some of your favorite actors",
    ['Leonardo DiCaprio', 'Tom Hanks', 'Scarlett Johansson', 'Emma Watson', 'Shah Rukh Khan', 'Ranbir Kapoor']
)

# ------------------------ 12. Button ------------------------
if st.button("🎯 Recommend Movies"):
    st.balloons()
    st.markdown("## 🔮 Top Recommendations for You")
    
    # Fake logic for demonstration
    recommendations = [
        "Inception", "The Matrix", "Interstellar", "La La Land", 
        "Zindagi Na Milegi Dobara", "The Pursuit of Happyness"
    ]
    
    selected = random.sample(recommendations, 3)
    
    for movie in selected:
        st.success(f"🎬 {movie}")

# ------------------------ 13. Text Input ------------------------
user_name = st.text_input("Enter your name:")
if user_name:
    st.write(f"Hello, **{user_name}**! Enjoy your personalized suggestions.")

# ------------------------ 14. Slider ------------------------
year_range = st.slider("Select Year Range of Release", 1990, 2025, (2005, 2023))
st.write(f"Filtering movies released between **{year_range[0]}** and **{year_range[1]}**.")

# ------------------------ Footer ------------------------
st.markdown("---")
st.markdown("© 2025 CineMatch AI | Built with  using Streamlit")
