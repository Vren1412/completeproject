import streamlit  as st
import pandas as pd
#1 title
st.title("Real - Time Movie Recommendation using Ai")
#6 imgload
st.image('bg.jpg',width=700)
#2 header
st.header('The Best Movie Recommend in the world')
#3. Subheader
st.subheader('its a Ai recommend')
#4. text
st.text("let's  Start")
#5. File to upload .csv file
uploadfile = st.file_uploader('upload .csv files only',type=['csv'])

if uploadfile is not None:
    dataFram=pd.read_csv(uploadfile)
    st.success('uploaded csv file Successfully..')
    st.dataframe(dataFram)
    #7 imgload
    st.write('File Name is ::', uploadfile.name)
    st.write('File  Shape  ::', dataFram.shape)
    st.write('colums  Data ::',dataFram.columns.tolist())

    st.subheader("Let's Start the Preprocessing......")
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
    st.write('Data : ',dataFram.describe())
    
    st.write('Data Visualization')
    #8 visual
    # fig1, ax1 = plt.subplots()
    # sns.histplot(dataFram['rating'],bins=10, kde=True , ax=ax1, color='skyblue')
    # ax1.set_xlabel("Rating")
    # ax1.set_ylabel("Count")
    # ax1.set_title("Rating Counts of Movies")
    # st.pyplot(fig1)
    #9. checkbox
    st.checkbox("select the Checkboxs for Accept the dataset")
    st.checkbox("select the Checkboxs for Accept the Rating data ")
    st.checkbox("select the Checkboxs for Accept the Movie data")
    #10 radio
    Sg= st.radio("Select thr Dataset colums: ",
        ['User_id', 'Movie_id','Movie_title', 'Rating'])
    if Sg is not None:
        st.success(Sg)
    #11 selectbox
    dat=st.selectbox("Select thr Dataset colums: ", 
            ['User_id', 'Movie_id','Movie_title', 'Rating'])
    if dat is not None:
        st.success(dat)
    #12 multi select box
    
    da=st.multiselect("Select the multi select  colums: ", 
            ['User_id', 'Movie_id','Movie_title', 'Rating'])
    if da is not None:
        st.success(len(da))
    #13 buttons
    stbutton = st.button("Register")
    if st.button("Login"):
        st.success('Login successfully')
    #14 text_input
    Stname=st.text_input("enter the name")
    if st.button("Submit"):
        name=Stname.title()
        st.success('Data Submited successfully')
        st.write("Your Name is :: ",name)
    




else:
    st.warning('You Can Uplpoad Only For .CSV File Format')
    st.error('file was not uploaded..')
    exc=FileNotFoundError()
    st.exception(exc)


#run the program
#streamlit run Abc.py