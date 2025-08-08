import streamlit as st
import sqlite3

def create_connection():
    conn = sqlite3.connect("Students.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            Phone TEXT,
            gender TEXT,
            address TEXT,
            Dob TEXT,
            Course TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_Student(name,email,phone,gender,address,Dob,course):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Students(name,email,phone,gender,address,Dob,course) values(?, ?, ?, ?, ?, ?, ? )""",
        (name,email,phone,gender,address,Dob,course)
        )
    conn.commit()
    conn.close()

def fetch_all_students():
    conn=create_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students")
    data=cursor.fetchall()
    conn.close()
    return data

st.set_page_config(page_title="Student Registration", layout="centered")
st.title(" Student Registration Form")
menu = st.sidebar.selectbox("Menu",
["Register", "View Registered Students"])

create_table()
with st.form("student_form"):
    name= st.text_input("Name")
    email =st.text_input("Email")
    phone=st.text_input("Phone Number")
    gender=st.selectbox("Gender", ["Male", "Female", "Other"])
    Dob=st.date_input("Date of Birth")
    address=st.text_area("Address")
    course=st.selectbox("Course", ["Fashion Theory", "Runway Science", "Style & Drip Analytics"])
    submitted=st.form_submit_button("Register")
    if submitted:
        insert_Student(name, email, phone, gender, Dob, address, course)
        st.success(f"Welcome aboard, (name)! Your fashion journey begins. ")

