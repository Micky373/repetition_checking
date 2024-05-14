# Importing useful libraries
import streamlit as st # For UI related tasks
import pandas as pd # FOr dataframe related tasks
# For operating system related tasks
import sys 
sys.path.append('..')
import os

from scripts import utils # For useful functions


# A function to read a file
def read_file(file_name):

    # Getting the file name and extension
    name = file_name.name
    extension = name.split('.')[-1]

    # Save the uploaded file to a temporary location
    temporary_file = f"temp_uploaded_file.{extension}"
    
    # Saving the uploaded file into a temporary file
    with open(temporary_file, "wb") as temp_file:
        temp_file.write(file_name.getbuffer())

    # Checking for the extension and read the file accordingly
    if extension == 'xls':
        df = utils.read_excel_file(temporary_file)
    
    elif extension == 'xlsx':
        df = pd.read_excel(temporary_file)

    else:
        df = pd.read_csv(temporary_file)

    # Remove the temporary file
    os.remove(temporary_file)

    # Returning the datframe
    return df

# Creating a title and icon to the webpage
st.set_page_config(
    page_title="Repeting Users Checking",
    page_icon="📚"
)

#  A header for the page
st.header("User Uniqueness Checking Simple App")

# A sub heading
st.subheader("Before Data Uploading Section")

# A file uploading area where we can upload our old data
before_file = st.file_uploader(
    'Please Upload the file containing the old data',
    type = ['csv','xls','xlsx']
)

# A sub heading
st.subheader("After Data Uploading Section")

# A file uploading section where we can upload our latest data
after_file = st.file_uploader(
    'Please Upload the file containing the latest data',
    type = ['csv','xls','xlsx']
)

# A button click action
if st.button('Analyse'):

    # Check if both the latest and old data are uploaded
    if before_file and after_file:
        
        # Reading the data
        with st.spinner("Reading the data"):

            before_df = read_file(before_file)
            after_df = read_file(after_file)

            st.subheader("Before Data")

            st.dataframe(before_df)

            st.subheader("After Data")

            st.dataframe(after_df)
        
        # Analyzing the data
        with st.spinner("Analysing"):

            try:

                before_emails = set(list(before_df['Email'].values))
                after_emails = set(list(after_df['Email'].values))

                # Finding unique users
                unique_users_before = before_emails - after_emails
                unique_users_after = after_emails - before_emails

                # Finding the repeting users
                repeting_users = after_emails.intersection(before_emails)

                temp_data = after_df['Email'].value_counts()
                temp_data = temp_data.reset_index()

                st.success(f'There are {len(repeting_users)} number of repeting users')

                st.success(f'There are {len(unique_users_after)} number of unique users out of {temp_data.shape[0]} users')

            except:

                st.warning("One of the data you uploaded doesn't have an Email column so please upload a data that contain Email column")

    else:

        st.warning("Upload first both the before and after data")