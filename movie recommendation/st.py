import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#t1 title
st.title("Real - Time Movie Recommendation using AI")
#6 imgload
st.image('av.jpg',width=500)
#t2 header
st.header("The best movie Recommendation in the world")
#3. Subheader
st.subheader("its a AI recommend")
#Text
st.text("lets start")
#5. file to uplod .csv
uploadfile = st.file_uploader('upload.csv files only', type=['csv'])

if uploadfile is not None:
    dataFram=pd.read_csv(uploadfile)
    st.success('uploaded csv file Succesfully')
    st.subheader("data uploaded succesfully..")
    st.dataframe(dataFram)
    #7. write
    st.write('File Name is ::', uploadfile.name)
    st.write('File Shape ::', dataFram.shape)
    st.write('colums Data ::', dataFram.columns.tolist())
    
    st.subheader("Lets start the preprocessing...........")
    dataFram.dropna(inplace=True)
    dataFram['user_id']=dataFram['user_id'].astype(int)
    dataFram['movie_id']=dataFram['movie_id'].astype(int)
    dataFram['rating']=dataFram['rating'].astype(float)
    st.write('data cleaning')
    st.dataframe(dataFram)
    st.write('First 5 rows')
    st.dataframe(dataFram.head())
    st.write('Last 5 rows')
    st.dataframe(dataFram.tail())
    st.write('Data :',dataFram.describe())
    #8 visualization
    st.write('Data Visualization')
    fig1, ax1= plt.subplots()
    sns.histplot(dataFram['rating'],bins=10, kde=True, ax=ax1, color = 'green')
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Count")
    ax1.set_title("Representation of Rating Counts of Movies")
    st.pyplot(fig1)
    #9 checkbox
    st.checkbox("select the Checkboxs for Accept the Dataset")
    st.checkbox("select the Checkboxs for Accept the Rating data")
    st.checkbox("select the Checkboxs for Accept the Movie data")
    #10 radiobutton
    Sg=st.radio("Select the dataset colums:",['user_id', 'movie_id','movie_title','rating'])
    if Sg is not None:
        st.success(Sg)
    #11 selectbox
    dat=st.selectbox("Select the dataset colums:",['user_id', 'movie_id','movie_title','rating'])
    if dat is not None:
        st.success(dat)

    #12 multiselect box
    da=st.multiselect("Select the dataset colums:",['user_id', 'movie_id','movie_title','rating'])
    if da is not None:
        st.success(len(da))
    #13 buttons
    stbutton=st.button("Register")
    if st.button("Login"):
        st.success('Login Successfully')
    #14 input field
    Stname=st.text_input("enter the name")
    if st.button("Submit"):
        name=Stname.title()
        st.success('data submited Successfully')
        st.write("Your Name is :: ",name)



else:
    st.warning('You Can Upload only .CSV File Error')
    st.error('file was not uploaded....')
    exc=FileNotFoundError()
    st.exception(exc)
#run the program
#streamlit run st.py