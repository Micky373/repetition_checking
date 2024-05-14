# Importing useful libraries
import streamlit as st
import pandas as pd
import sys
sys.path.append('..')
from scripts import utils
import os

def read_file(file_name):

    name = file_name.name
    extension = name.split('.')[-1]

    # Save the uploaded file to a temporary location
    temporary_file = f"temp_uploaded_file.{extension}"

    with open(temporary_file, "wb") as temp_file:
        temp_file.write(file_name.getbuffer())

    if extension == 'xls':
        df = utils.read_excel_file(temporary_file)
    
    elif extension == 'xlsx':
        df = pd.read_excel(temporary_file)

    else:
        df = pd.read_csv(temporary_file)

    # Remove the temporary file
    os.remove(temporary_file)

    return df

st.set_page_config(
    page_title="Repeting Users Checking",
    page_icon="📚"
)

st.header("User Uniqueness Checking Simple App")

st.subheader("Before Data Uploading Section")

before_file = st.file_uploader(
    'Please Upload the file containing the old data',
    type = ['csv','xls','xlsx']
)

st.subheader("After Data Uploading Section")

after_file = st.file_uploader(
    'Please Upload the file containing the latest data',
    type = ['csv','xls','xlsx']
)

if st.button('Analyse'):

    if before_file and after_file:

        with st.spinner("Reading the data"):

            before_df = read_file(before_file)
            after_df = read_file(after_file)

            st.subheader("Before Data")

            st.dataframe(before_df)

            st.subheader("After Data")

            st.dataframe(after_df)
        
        with st.spinner("Analysing"):

            try:

                before_emails = set(list(before_df['Email'].values))
                after_emails = set(list(after_df['Email'].values))

                # Find unique users
                unique_users_before = before_emails - after_emails
                unique_users_after = after_emails - before_emails

                repeting_users = after_emails.intersection(before_emails)

                temp_data = after_df['Email'].value_counts()
                temp_data = temp_data.reset_index()

                st.success(f'There are {len(repeting_users)} number of repeting users')

                st.success(f'There are {len(unique_users_after)} number of unique users out of {temp_data.shape[0]} users')

            except:

                st.warning("One of the data you uploaded doesn't have an Email column so please upload a data that contain Email column")

    else:

        st.warning("Upload first both the before and after data")