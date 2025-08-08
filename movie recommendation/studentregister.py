import streamlit as st
import sqlite3

def create_connection():
    conn = sqlite3.connect("students.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            gender TEXT,
            dob TEXT,
            address TEXT,
            course TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_student(name, email, phone, gender, dob, address, course):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students 
        
        
        
                   (name, email, phone, gender, dob, address, course)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, email, phone, gender, dob, address, course)
    )
    conn.commit()
    conn.close()

def fetch_all_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return data

st.set_page_config(page_title="Student Registration", layout="centered")
st.title(" Student Registration Form")

menu = st.sidebar.selectbox("Menu",
     ["Register", "View Registered Students"])

create_table()

if menu == "Register":
    st.subheader(" Fill in the Details Below:")

    with st.form("registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth")
        address = st.text_area("Address")
        course = st.selectbox("Course Enrolled", ["B.Tech", "B.Sc", "B.Com", "M.Tech", "MBA", "Other"])
        
        submitted = st.form_submit_button("Register")

        if submitted:
            if name and email and phone:
                insert_student(name, email, phone, gender, str(dob), address, course)
                st.success(" Student registered successfully!")
            else:
                st.warning(" Please fill out all required fields.")

elif menu == "View Registered Students":
    st.subheader(" All Registered Students")
    students = fetch_all_students()
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No students registered yet.")