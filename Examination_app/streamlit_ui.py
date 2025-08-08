import streamlit as st
import requests
import base64

FASTAPI_URL = "http://localhost:8000"
FLASK_UI_URL = "http://localhost:5000"

# ---------- Background Image Setup ----------
def set_bg(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    bg_css = f"""
    <style>
    [data-testid="stApp"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: black !important;
    }}
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stButton button {{
        background-color: rgba(255, 255, 255, 0.9);
        color: black !important;
    }}
    .stMarkdown, .stHeader {{
        background-color: rgba(255, 255, 255, 0.75);
        padding: 0.5rem;
        border-radius: 8px;
        color: black !important;
    }}
    label, h1, h2, h3, h4, h5, h6, p, span {{
        color: black !important;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# 🔽 Set background (place image in your folder, e.g., "assets/exam_bg.jpg")
set_bg("assets/exam_bg.jpg")  # Make sure this path exists

st.markdown("<h1 style='color: black;'>Exam Management System</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Choose Action", ["Home", "Register Student", "Start Quiz", "Contact Us"])

# ------------------ HOME ------------------ #
if menu == "Home":
    st.markdown(f"<p style='color: black;'><a href='{FLASK_UI_URL}'>Go to Home Page</a></p>", unsafe_allow_html=True)

# ------------------ REGISTER ------------------ #
elif menu == "Register Student":
    st.markdown("<h3 style='color: black;'>Student Registration</h3>", unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {"name": name, "email": email, "password": password}
        res = requests.post(f"{FASTAPI_URL}/student/register", json=payload)
        if res.status_code == 200:
            st.success("Registered Successfully")
        else:
            st.error(f"Failed: {res.json().get('detail', 'Error')}")

# ------------------ START QUIZ ------------------ #
elif menu == "Start Quiz":
    st.markdown("<h3 style='color: black;'>Start Quiz</h3>", unsafe_allow_html=True)

    student_id = st.text_input("Student ID")
    topic = st.text_input("Topic")

    # Initialize session state
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Fetch questions button
    if st.button("Fetch Questions"):
        res = requests.get(f"{FASTAPI_URL}/quiz/questions/{topic}")
        if res.status_code == 200:
            st.session_state.questions = res.json()
            st.session_state.answers = {}
        else:
            st.warning("No questions found for this topic.")

    # Show questions if available
    if st.session_state.questions:
        for q in st.session_state.questions:
            st.markdown(f"<p style='color: black;'>Q{q['id']}: {q['question_text']}</p>", unsafe_allow_html=True)

            options = {
                "A": q['option_a'],
                "B": q['option_b'],
                "C": q['option_c'],
                "D": q['option_d']
            }

            selected = st.radio(
                f"Choose answer for Q{q['id']}",
                options.items(),
                format_func=lambda x: f"{x[0]}. {x[1]}",
                key=f"question_{q['id']}"
            )

            st.session_state.answers[q['id']] = selected[0]

        # Submit answers button
        if st.button("Submit Answers"):
            q_ids = list(st.session_state.answers.keys())
            selected_letters = list(st.session_state.answers.values())

            res = requests.post(f"{FASTAPI_URL}/quiz/submit", json={
                "student_id": student_id,
                "topic": topic,
                "questions": q_ids,
                "answers": selected_letters
            })

            if res.status_code == 200:
                result = res.json()
                st.success(f"Score: {result['score']}")
                st.info(f"Feedback: {result['feedback']}")
                st.session_state.questions = []
                st.session_state.answers = {}
            else:
                st.error("Failed to submit answers.")

# ------------------ CONTACT US ------------------ #
elif menu == "Contact Us":
    st.markdown("<h3 style='color: black;'>Contact Form</h3>", unsafe_allow_html=True)
    name = st.text_input("Name", key="contact_name")
    email = st.text_input("Email", key="contact_email")
    message = st.text_area("Message", key="contact_message")

    if st.button("Send Message"):
        res = requests.post(f"{FASTAPI_URL}/contact", json={
            "name": name,
            "email": email,
            "message": message
        })
        if res.status_code == 200:
            st.success("Message sent and stored!")
        else:
            st.error("Failed to send message.")

#streamlit run streamlit_ui.py