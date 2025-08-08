import streamlit as st
import pandas as pd
import os
import json
import pickle
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer

USERS_FILE = "users.json"
MODEL_FILE = "movie_similarity.pkl"
MOVIE_FILE = "Movie_Id_Titles.csv"
RATINGS_FILE = "ratings.csv"

st.set_page_config(page_title=" Movie Recommender", layout="centered")
st.title(" Real-time Movie Recommender with ML + Ollama")

@st.cache_data
def load_movies():
    return pd.read_csv(MOVIE_FILE)

movies_df = load_movies()

def generate_sample_ratings():
    import random
    if not os.path.exists(RATINGS_FILE):
        user_ids = list(range(1, 6))
        sample_size = min(30, len(movies_df))
        movie_ids = movies_df['movie_id'].sample(sample_size, replace=False).tolist()
        data = []
        for u in user_ids:
            for m in random.sample(movie_ids, min(5, len(movie_ids))):
                data.append([u, m, random.randint(1, 5)])
        df = pd.DataFrame(data, columns=['user_id', 'movie_id', 'rating'])
        df.to_csv(RATINGS_FILE, index=False)

generate_sample_ratings()

def train_model():
    df = pd.read_csv(RATINGS_FILE)
    pivot = df.pivot_table(index='user_id', columns='movie_id', values='rating')
    imputer = SimpleImputer(strategy='mean')
    rating_filled = imputer.fit_transform(pivot)
    similarity = cosine_similarity(rating_filled.T)
    movie_ids = pivot.columns.tolist()
    model_data = {"similarity": similarity, "movie_ids": movie_ids}
    pickle.dump(model_data, open(MODEL_FILE, "wb"))

if not os.path.exists(MODEL_FILE):
    train_model()

model_data = pickle.load(open(MODEL_FILE, "rb"))
similarity = model_data['similarity']
movie_ids = model_data['movie_ids']

def load_users():
    if not os.path.exists(USERS_FILE):
        json.dump({}, open(USERS_FILE, 'w'))
    return json.load(open(USERS_FILE))

def save_users(users):
    json.dump(users, open(USERS_FILE, 'w'))

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "user_id": len(users) + 1}
    save_users(users)
    return True

def validate_login(username, password):
    users = load_users()
    return users.get(username, {}).get("password") == password

def recommend_movies(user_id, top_n=5):
    ratings = pd.read_csv(RATINGS_FILE)
    user_rated = ratings[ratings['user_id'] == user_id]
    scored_movies = {}

    for _, row in user_rated.iterrows():
        try:
            idx = movie_ids.index(row['movie_id'])
        except ValueError:
            continue
        sim_scores = list(enumerate(similarity[idx]))
        for i, score in sim_scores:
            m_id = movie_ids[i]
            if m_id not in user_rated['movie_id'].values:
                scored_movies[m_id] = scored_movies.get(m_id, 0) + score * row['rating']

    top = sorted(scored_movies.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [
        movies_df[movies_df['movie_id'] == mid]['movie_title'].values[0]
        for mid, _ in top if not movies_df[movies_df['movie_id'] == mid].empty
    ]

def get_ollama_response(prompt):
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, headers=headers, json=data)
        return r.json()['response']
    except Exception as e:
        return f"Error talking to LLaMA: {e}"

menu = st.sidebar.selectbox("Navigation", ["Login", "Register"])
session = st.session_state

if 'logged_in' not in session:
    session.logged_in = False
    session.username = ''
    session.user_id = None

if menu == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful. Please login.")
        else:
            st.error("Username already exists.")

elif menu == "Login":
    st.subheader("Login to your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_login(username, password):
            session.logged_in = True
            session.username = username
            session.user_id = load_users()[username]['user_id']
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")
 
if session.logged_in:
    st.success(f"Logged in as {session.username}")
    st.subheader(" Movie Recommendations")
    if st.button("Get Recommendations"):
        recommendations = recommend_movies(session.user_id)
        st.write("Top Movies You May Like:")
        for m in recommendations:
            st.markdown(f"- {m}")

    st.subheader(" Ask LLaMA for Recommendations")
    liked_movies = st.text_input("Movies you liked (comma-separated)")
    if st.button("Ask LLaMA"):
        prompt = f"I liked these movies: {liked_movies}. Based on my taste, recommend me some good movies."
        response = get_ollama_response(prompt)
        st.markdown("**LLaMA Recommends:**")
        st.write(response)
