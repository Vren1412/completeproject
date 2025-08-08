import streamlit as st
from PIL import Image

# 1. Title
st.title(" Streamlit Component Showcase")

# 2. Header and Subheader
st.header(" All UI Widgets in One Page")
st.subheader(" Learn Streamlit Basics Quickly")

# 3. Text
st.text("This is basic text. It’s useful for instructions or labels.")

# 4. Markdown
st.markdown("**This is bold text in markdown**")
st.markdown("*Italic text*, `code`, and [links](https://streamlit.io)")

# 5. Status Messages
st.success("Success: Everything worked!")
st.info("Info: This is some informational text.")
st.warning("Warning: Something might be off.")
st.error("Error: Something went wrong.")
try:
    1 / 0
except ZeroDivisionError as e:
    st.exception(e)

# 6. Write
st.write("Using `st.write()` to render Python objects:")
st.write({"Name": "Streamlit", "Type": "Library", "Rating": 5})

# 7. Display Images
st.subheader(" Displaying Image")
img_url = "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png"
st.image(img_url, caption="Streamlit Logo", use_column_width=True)

# 8. Checkbox
st.subheader(" Checkbox")
show_code = st.checkbox("Show source code?")
if show_code:
    st.code("print('Hello Streamlit!')")

# 9. Radio Button
st.subheader(" Radio Button")
fav_lang = st.radio("Pick your favorite programming language:", ["Python", "JavaScript", "Rust"])
st.write(f"You selected: {fav_lang}")

# 10. Selection Box
st.subheader(" Select Box")
os_choice = st.selectbox("Which operating system do you use?", ["Windows", "Linux", "macOS"])
st.write("You selected:", os_choice)

# 11. Multi-Select Box
st.subheader(" Multi-Select Box")
features = st.multiselect("What features do you like in Streamlit?", ["Simplicity", "Speed", "Widgets", "Open Source"])
st.write("You selected:", features)

# 12. Button
st.subheader(" Button")
if st.button("Click Me"):
    st.success("You clicked the button!")

# 13. Text Input
st.subheader(" Text Input")
name = st.text_input("What's your name?", "")
if name:
    st.write(f"Hello, {name}!")

# 14. Slider
st.subheader(" Slider")
age = st.slider("Select your age:", 1, 100, 25)
st.write(f"Your age is: {age}")
