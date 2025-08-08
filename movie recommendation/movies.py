import streamlit as st
import pandas as pd
#t1 title
st.title("Real - Time Movie Recommendation using AI")
#t2 header
st.header("The best movie Recommendation in the world")
#3. Subheader
st.subheader("its a AI recommend")
#Text
st.text("lets start")
#5. file to uplod .csv
uploadfile = st.file_uploader('upload.csv files only', type=['csv'])
#run the program
#streamlit run mov.py