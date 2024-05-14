# Importing useful libraries
import pandas as pd # For data related tasks

# For data visualization tasks
import matplotlib.pyplot as plt
import seaborn as sns

from ydata_profiling import ProfileReport # For automatic visualizations
from datetime import datetime# For date and time related tasks
import re # For regular expression related tasks
from urllib.parse import unquote # For URL related tasks
import OleFileIO_PL # For reading excel files
import os # For operating system related tasks
import ast # For list and string related tasks
from pandas import Timestamp # For time related tasks
import plotly.express as px # For visualization tasks

# A function to get the full name of the states
def get_country_name(code):

    # This is the data I got from https://gist.github.com/rogerallen/1583593
    state_lookup = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'DC': 'District of Columbia',
    'AS': 'American Samoa',
    'GU': 'Guam',
    'MP': 'Northern Mariana Islands',
    'PR': 'Puerto Rico',
    'UM': 'United States Minor Outlying Islands',
    'VI': 'U.S. Virgin Islands'
    }

    try:
        state_name = state_lookup[code]
    except:
        state_name = None


    return state_name

# A function to return click date 
def return_click_date(click_df,survey_emails):
    temp_data = []
    for survey_email in survey_emails:
        temp_data.append(list(click_df[click_df['Sub ID 5'] == survey_email]['Click Date'].values))
    return temp_data

# A function to calculate age of a person
def calculate_age(dob):
    year = dob.split('-')[0]
    month = dob.split('-')[1]
    date = dob.split('-')[2]
    today = datetime.today()
    age = today.year - int(year) - ((today.month, today.day) < (int(month), int(date)))
    return age

# A function for general visualization
def visualize(path,fig_name,title):

    # Reading the data
    data = pd.read_csv(path)

    # Clean up the column names to remove trailing spaces
    data.columns = data.columns.str.strip()

    # Convert date strings to actual day names for consistent ordering
    data['Day of the week'] = pd.Categorical(data['Day of the week'], categories=[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    
    # Dropping the date column for visualization part
    data.drop(
        columns = ['Date'],
        inplace = True
    )

    # Group data by Status and Date to calculate mean values for metrics
    grouped_data = data.groupby(['Status', 'Day of the week']).mean().reset_index()

    # Set the style of seaborn for better aesthetics
    sns.set(style="whitegrid")

    # Create a subplot environment
    plt.figure(figsize=(20, 10))

    # Plotting Total Revenue
    plt.subplot(3,2,1)
    sns.lineplot(x='Day of the week', y='Total Revenue', hue='Status', data=grouped_data, marker='o')
    plt.title('Effect on Total Revenue')
    plt.ylabel('Total Revenue')
    plt.xlabel('Day of the Week')

    # Plotting All click from cake
    plt.subplot(3,2,2)
    sns.lineplot(x='Day of the week', y='All click from cake', hue='Status', data=grouped_data, marker='o')
    plt.title('Effect on all clicks from cake')
    plt.ylabel('All Clicks from Cake')
    plt.xlabel('Day of the Week')

    # Plotting Registered as per survey takers
    plt.subplot(3,2,3)
    sns.lineplot(x='Day of the week', y='Registered as per survey takers', hue='Status', data=grouped_data, marker='o')
    plt.title('Effect on average registration')
    plt.ylabel('Registrations')
    plt.xlabel('Day of the Week')

    # Plotting Last page all clicks
    plt.subplot(3,2,4)
    sns.lineplot(x='Day of the week', y='Last page all clicks', hue='Status', data=grouped_data, marker='o')
    plt.title('Effect on last page click')
    plt.ylabel('Last Page Clicks')
    plt.xlabel('Day of the Week')

    # Plotting Last page all clicks
    plt.subplot(3,2,5)
    sns.lineplot(x='Day of the week', y='Revenue Per User', hue='Status', data=grouped_data, marker='o')
    plt.title('Effect on revenue per user')
    plt.ylabel('Revenue Per User')
    plt.xlabel('Day of the Week')

    # Adjust layout to avoid overlaps
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Adding a title 
    plt.suptitle(title,fontsize=25)

    # Saving the figure
    plt.savefig(fig_name)

    # Show the plots
    plt.show()

# Creating a function for general visualization
def visualize_2(path,fig_name,title,final_data = False):
    
    # Reading the data
    if final_data:
        data = path
    else:
        data = pd.read_csv(path)

    # Clean up the column names to removing trailing spaces
    data.columns = data.columns.str.strip()

    # Convert date strings to actual day names for consistent ordering
    data['Day of the week'] = pd.Categorical(data['Day of the week'], categories=[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    
    # Dropping the date column for visualization part
    data.drop(
        columns = ['Date'],
        inplace = True
    )
    
    # Create a subplot environment
    plt.figure(figsize=(20, 10))

    # Sum total revenue for 'Before' and 'After'
    total_revenue = data.groupby('Status')['Total Revenue'].sum().reset_index()
    mean_revenue_per_user = data.groupby('Status')['Revenue Per User'].mean().reset_index()

    # Calculate percentage increase for total revenue
    if total_revenue['Total Revenue'].iloc[0] != 0:  # To avoid division by zero
        percent_increase_total_revenue = ((total_revenue['Total Revenue'].iloc[0] - total_revenue['Total Revenue'].iloc[1]) / 
                            total_revenue['Total Revenue'].iloc[1]) * 100
    else:
        percent_increase_total_revenue = float('inf')  # Infinite increase if initial revenue is zero

    # Calculate percentage increase for revenue per user
    if mean_revenue_per_user['Revenue Per User'].iloc[0] != 0:  # To avoid division by zero
        percent_increase_revenue_per_user = ((mean_revenue_per_user['Revenue Per User'].iloc[0]\
                                               - mean_revenue_per_user['Revenue Per User'].iloc[1]) / 
                            mean_revenue_per_user['Revenue Per User'].iloc[1]) * 100
    else:
        percent_increase_revenue_per_user = float('inf')  # Infinite increase if initial revenue per user is zero


    # Create a bar plot for total revenue
    plt.subplot(1,2,1)
    bar_plot = sns.barplot(x='Status', y='Total Revenue', data=total_revenue)
    plt.title('Comparison of Total Revenue Before and After Intervention')
    plt.ylabel('Total Revenue')
    plt.xlabel('Status')

    # Annotate each bar with the value of the revenue
    for bar in bar_plot.patches:
        bar_plot.annotate(format(bar.get_height(), '.2f'),
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                        ha='center', va='center',
                        size=20, xytext=(0, 8),
                        textcoords='offset points')

    # Annotate percent increase directly on the plot
    plt.text(0, total_revenue['Total Revenue'].max() / 2, f'{percent_increase_total_revenue:.2f}%\nIncrease', 
            fontsize=23, ha='center', color='green',fontweight = 'bold')


    plt.subplot(1,2,2)
    bar_plot_2 = sns.barplot(x='Status', y='Revenue Per User', data=mean_revenue_per_user)
    plt.title('Comparison of average revenue per user Before and After Intervention')
    plt.ylabel('Average revenue per user')
    plt.xlabel('Status')

    # Annotate each bar with the value of the revenue per user
    for bar in bar_plot_2.patches:
        bar_plot_2.annotate(format(bar.get_height(), '.2f'),
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                        ha='center', va='center',
                        size=20, xytext=(0, 8),
                        textcoords='offset points')
        
    # Annotate percent increase directly on the plot
    plt.text(0, mean_revenue_per_user['Revenue Per User'].max() / 2, f'{percent_increase_revenue_per_user:.2f}%\nIncrease', 
            fontsize=23, ha='center', color='green',fontweight = 'bold')
    
    # Adjust layout to avoid overlaps
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Adding a title 
    plt.suptitle(title,fontsize=25)

    # Saving the figure
    plt.savefig(fig_name)

    # Show the plot
    plt.show()

# Creating a function to return the day name
def return_day_name(date_string):
    # The date format provided by the user is YY-MM-DD, which corresponds to the format '%y-%m-%d' in datetime.strptime
    date_format = '%Y-%m-%d'

    # Parse the date string into a datetime object
    date_object = datetime.strptime(str(date_string).split(' ')[0].strip(), date_format)

    # Get the day of the week, where Monday is 0 and Sunday is 6
    day_of_the_week = date_object.weekday()

    # Map the day of the week to its name
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = days[day_of_the_week]

    return day_name

# Creating a function to create a general visualization
def create_general_visualization(path,file_name):

    # Reading the data
    data = pd.read_csv(path)
    data['Status'] = data['Status'].apply(lambda x:0 if x=='Before' else 1)

    # Vizualizing the whole data
    profile = ProfileReport(
        data,
        explorative = True
    )
    profile.to_file(file_name)
    print("***Done!!!***")

# A function to parse email from our url
def find_emails(text):

    email_pattern = r'email=([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'

    emails = re.findall(email_pattern, unquote(text))

    if len(emails) > 0 and 'email' in text.lower():
        if len(set(emails)) > 1:
            return emails
        return emails[0]
    elif len(emails) > 0 and 's5' in text.lower():
        if len(set(emails)) > 1:
            return emails
        return emails[0]
    else:
        return 'Not Found'
    
# A function to get a data containing weird emails
def get_abnormal_emails_data(survey_data_path,click_data_path):

    click_data = pd.read_csv(click_data_path)

    # Reading the before and after data and taking only the 18453
    survey_data = read_excel_file(survey_data_path)

    survey_emails = list(set(survey_data['Email'].values))
    click_data['user_emails'] = click_data['Request URL'].apply(find_emails)

    click_emails = list(set(click_data['user_emails'].values))
    weird_emails = []
    for email in survey_emails:
        if email not in click_emails:
            weird_emails.append(email)
            
    data = {
        'Emails from survey data' : weird_emails,
        'Emails from the banner link' : [],
        'URL of the banner' : []
    }

    for email in weird_emails:
        user_ip = list(set(list(survey_data[survey_data['Email'] == email]['IP Address'].values)))
        temp_email = []
        temp_urls = []
        for ip in user_ip:
            urls = list(set(list(click_data[click_data['IP Address'] == ip]['Request URL'].values)))

            if len(urls) > 0:
                for url in urls:
                    temp_urls.append(url)
                    temp_email.append(find_emails(url))
            else:
                temp_urls.append('No URL found')
                temp_email.append('Not Found in the click data')
        
        temp_email = list(set(temp_email))
        if len(temp_email) > 1:
            data['Emails from the banner link'].append(temp_email)
        else:
            data['Emails from the banner link'].append(temp_email[0])

        temp_urls = list(set(temp_urls))
        if len(temp_urls) > 1:
            data['URL of the banner'].append(temp_urls)
        else:
            data['URL of the banner'].append(temp_urls[0])

    df = pd.DataFrame(data)

    return df

# A function to get user analytics
def user_analysis(day_before_path,day_after_path,day_after_click_data_path,before_date,after_date):
       
    # Reading the before and after data and taking only the 18453
    before = read_excel_file(day_before_path)
    after = read_excel_file(day_after_path)

    before = before[before['Revenue Tracker ID'].isin([7750,8866,8867,8895])]

    after = after[after['Revenue Tracker ID'].isin([7750,8866,8867,8895])]

    # Getting the total email addresses
    before_emails = (list(before['Email'].values))
    after_emails = (list(after['Email'].values))

    # Getting the emails that repeated
    temp_emails = []
    for email in before_emails:
        if email in after_emails:
            temp_emails.append(email)

    # Let us see data of the repeated user on April 23 and take the latest time
    temp_df_before = before[before['Email'].isin(temp_emails)][['Email','Revenue Tracker ID','Updated At']].sort_values('Email')
    temp_df_before = temp_df_before.groupby('Email').min()
    temp_df_before = temp_df_before.reset_index()

    # Let us see data of the repeated user and take the latest time
    temp_df_after = after[after['Email'].isin(temp_emails)][['Email','Revenue Tracker ID','Updated At']].sort_values('Email')
    temp_df_after = temp_df_after.groupby('Email').min()
    temp_df_after = temp_df_after.reset_index()

    # Let us get the users that get back after 24hrs and still registered again
    repeated_emails = []
    for email in temp_emails:
        before_time = temp_df_before[temp_df_before['Email']==email]['Updated At'].values[0]
        after_time = temp_df_after[temp_df_after['Email']==email]['Updated At'].values[0]

        time_gap = datetime.strptime(after_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(before_time, '%Y-%m-%d %H:%M:%S')
        if abs(time_gap.total_seconds()) >= 86400:
            repeated_emails.append(email)

    repeated_df = temp_df_after[temp_df_after['Email'].isin(repeated_emails)][['Email','Updated At','Revenue Tracker ID']].sort_values('Email')

    print(f'From total of {after.shape[0]} registration, {len(temp_emails)} were repeated')
    print(f'From the above repeated registrations, {len(list(set(repeated_emails)))} users were registered again even after 24hrs')

    print("***********************************")
    print("---REPEATED REGISTRATION---")
    # Let us see how the repeated emails are distributed over the campaigns
    print(repeated_df['Revenue Tracker ID'].value_counts())
    print("***********************************")

    repeated_df[f'April {str(after_date)}'] = repeated_df['Updated At']
    repeated_df[f'April {str(before_date)}'] = temp_df_before['Updated At']
    data_to_be_saved = repeated_df[['Email',f'April {str(before_date)}',f'April {str(after_date)}','Revenue Tracker ID']]
    data_to_be_saved.to_csv(
        f'../synthesized_data/repeated_users_{str(after_date)}.csv',
        index = False
    )

    print(f'Saved to repeated_users_{str(after_date)}.csv')

    # Let us read the click data and see if there is issue in the request url for the repeated users

    # Reading the data
    click_data = pd.read_csv(day_after_click_data_path)

    # Let us get the emails from the url
    click_data['user_email'] = click_data['Request URL'].apply(find_emails)

    print("***********************************")
    print("---USERS THAT GOT ABNORMAL URL OR THAT WE DIDN'T GET THE DATA FROM OUR CLICK DATA---")
    # Let us see if all the emails registered on April 24 are found in the click data
    abnormal_link_sent_users = []
    for email in list(set(repeated_emails)):
        if email not in click_data['user_email'].values:
            abnormal_link_sent_users.append(email)
            print(email)
    print("***********************************")

    # Gettin the abnormal emails
    df = get_abnormal_emails_data(day_after_path,day_after_click_data_path)
    df = df[df['Emails from survey data'].isin(abnormal_link_sent_users)]
    df.to_csv(
        f'../synthesized_data/abnormal_emails_{str(after_date)}.csv',
        index = False
    )

# Reading excel file
def read_excel_file(path):
    with open(path,'rb') as file:
        ole = OleFileIO_PL.OleFileIO(file)
        if ole.exists('Workbook'):
            d = ole.openstream('Workbook')
            data=pd.read_excel(d,engine='xlrd')
    return data

# A function that gives us successful users given the survey data and successful users data
def get_success_users(success_users_data_path,survey_data_path,date):    

    data_frames = []
    parent_path = success_users_data_path

    for child_path in os.listdir(parent_path):
        df = pd.read_csv(parent_path + child_path)
        data_frames.append(df)

    survey_data = read_excel_file(survey_data_path)

    final_data = pd.concat(data_frames,axis = 0)

    final_data.to_csv(
        f'../synthesized_data/click_data/click_data_success_{str(date)}.csv',
        index = False
    )

    survey_emails = list(set(survey_data['Email'].values))
    success_emails = list(set(list(final_data['Sub ID 5'].values)))
    unique_emails = []

    for email in success_emails:
        if email not in survey_emails:
            unique_emails.append(email)

    success_emails = [email for email in success_emails if email not in unique_emails]

    df = survey_data[survey_data['Email'].isin(success_emails)]

    df.drop_duplicates(subset=['Email'], keep='first', inplace=True)

    df.drop(columns=['Created At','Updated At'], inplace=True)

    df['State'] = df['State'].apply(get_country_name)

    survey_emails = list(df['Email'].values)
    df['Sessions'] = return_click_date(final_data,survey_emails)

    # Let us change the birth date column by age
    df['Birthdate'] = df['Birthdate'].apply(calculate_age)
    df.rename(columns={'Birthdate': 'Age'}, inplace=True)

    # Let us concatenate the first and last name into full name
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
    df['First Name'] = df['Full Name']
    df.drop(columns=['Last Name','Full Name'], inplace=True)
    df.rename(columns={'First Name': 'Full Name'}, inplace=True)

    columns_to_be_dropped = [
    'ID',
    'Affiliate ID',
    'Revenue Tracker ID',
    'Address1',
    'Address2',
    'Phone',
    'S3',
    'S4',
    'S5',
    'Response',
    'IP Address',
    'All Inbox Status'
    ]

    usefull_columns = []
    for column in list(df.columns):
        if column not in columns_to_be_dropped:
            usefull_columns.append(column)

    df = df[usefull_columns]
    
    df['Gender'] = df['Gender'].apply(lambda gender:gender.upper())

    df.to_csv(
        f'../synthesized_data/success_data/last_page_april_{date}.csv',
        index = False
    )

    return df

# Creating a before and after click data
def create_click_data_df(list_of_before_dates,status):
    data_frames = []
    for date in list_of_before_dates:
        df = pd.read_csv(f'../synthesized_data/click_data/click_data_success_{date}.csv')
        data_frames.append(df)

    df = pd.concat(data_frames,axis = 0)
    df.to_csv(
        f'../synthesized_data/{status}/click_data_success_{status}.csv',
        index = False
    )

# A function to create one csv survey data file
def create_survey_data_df(list_of_before_dates,status):
    data_frames = []
    for date in list_of_before_dates:
        df = pd.read_csv(f'../synthesized_data/success_data/last_page_april_{date}.csv')
        data_frames.append(df)

    df = pd.concat(data_frames,axis = 0)
    df.to_csv(
        f'../synthesized_data/{status}/survey_data_success_{status}.csv',
        index = False
    )

# A function to drop duplicates and create a sessions list
def drop_duplicates(status):
    df = pd.read_csv(f'../synthesized_data/{status}/survey_data_success_{status}.csv')
    temp_data = pd.DataFrame(
        df['Email'].value_counts()
    )
    temp_data = temp_data.reset_index()
    repeated_emails = list(temp_data[temp_data['count']>1]['Email'].values)
    df['Sessions'] = df['Sessions'].apply(ast.literal_eval)
    repeated_email_sessions = {}
    for email in repeated_emails:
        data = list(df[df['Email']==email]['Sessions'].values)
        sessions = [item for sublist in data for item in sublist]
        repeated_email_sessions[email] = sessions

    df.drop_duplicates(subset=['Email'], keep='first', inplace=True)
    for email in repeated_emails:
        df.loc[df['Email'] == email, 'Sessions'] = str(repeated_email_sessions[email])
    

    df.to_csv(
        f'../synthesized_data/{status}/survey_data_success_{status}.csv',
        index = False
    )

# A function to change string to date time stamp data type
def change_object_type_time_stamp(string_timestamps):

    # Use regular expressions to extract timestamps
    timestamps_str = re.findall(r"Timestamp\('([^']+)'", string_timestamps)

    # Convert string timestamps to Timestamp objects
    timestamps_list = [Timestamp(ts) for ts in timestamps_str]

    return (timestamps_list)

# A function that will return the time frame
def classify_hour(hour):
    if 6 <= hour <= 11:
        return 'Morning'
    elif 12 <= hour <= 17:
        return 'Afternoon'
    elif 18 <= hour <= 23:
        return 'Evening'
    else:
        return 'Night'

# Visualizing the six days analysis before and after the intervention   
def visualize_six_days(status,title):
    # Reading the data
    data = pd.read_csv(f'../synthesized_data/{status}/survey_data_success_{status}.csv')

    # Getting all the success sessions
    sessions = list(data['Sessions'].values)
    sessions = [ast.literal_eval(item)[0] for item in sessions]
    sessions = [datetime.strptime(date_string, '%m/%d/%y %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')\
                for date_string in sessions]
    # Changing the sessions time into 24hrs format
    completion_by_hour = [int(date_time_object.split(' ')[-1].split(':')[0]) for date_time_object in sessions]

    # Getting the time frames ( evening,night,morning,afternoon )
    completion_by_time_frame = [classify_hour(int(hour)) for hour in completion_by_hour ]

    data = {
        'hour of the day' : completion_by_hour,
        'time frame' : completion_by_time_frame
    }

    df = pd.DataFrame(data)

    completion_by_time_frame = df['time frame'].value_counts()
    completion_by_hour = df['hour of the day'].value_counts().sort_index()

    plt.figure(figsize=(20, 10))

    plt.subplot(1,2,1)
    completion_by_hour.plot(kind='bar')
    plt.title('Survey Completion by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Completions')
    plt.xticks(rotation=0)
    plt.savefig('../charts/hour_completion_rate_analysis.jpg')

    plt.subplot(1,2,2)
    completion_by_time_frame.plot(kind='pie', autopct='%1.2f%%')
    plt.savefig('../charts/hour_completion_rate_analysis_2.jpg')

    plt.suptitle(title,fontsize=25)

    plt.show()

# A function for graphical analysis of gender for six days
def gender_visualization_for_six_days(status,title):
    df = pd.read_csv(f'../synthesized_data/{status}/survey_data_success_{status}.csv')
    # Plotting the completion counts by gender

    gender_completion_counts = df['Gender'].value_counts()

    plt.figure(figsize=(20,10))

    plt.subplot(1,2,1)
    gender_completion_counts.plot(kind='bar')
    plt.title('Completion Counts by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Number of Completions')
    plt.xticks(rotation=0)

    plt.subplot(1,2,2)
    gender_completion_counts.plot(kind='pie', autopct='%1.2f%%', startangle=140, colors=['lightpink','blue'])
    plt.title('Completion Rates by Gender')
    plt.ylabel('')

    plt.savefig(f'../charts/gender_completion_rate_{status}.jpg')

    plt.suptitle(title,fontsize=25)
    
    plt.show()

# A function to anotate each bar in a bar chart
def anotate(bar):

    for p in bar.patches:
        bar.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points')

# A bar chart analysis for the age
def age_bar_chart_vizualization_six_days(title):

    df_before = pd.read_csv(f'../synthesized_data/before/survey_data_success_before.csv')
    df_after = pd.read_csv(f'../synthesized_data/after/survey_data_success_after.csv')

    # Creating age groups
    bins = [18,35, 45, 55, 65, float('inf')]
    labels = ['18-34', '35-44', '45-54', '55-64', '65+']
    df_before['Age Group'] = pd.cut(df_before['Age'], bins=bins, labels=labels, right=False)
    age_group_counts_before = df_before['Age Group'].value_counts().sort_index()

    # Creating age groups
    df_after['Age Group'] = pd.cut(df_after['Age'], bins=bins, labels=labels, right=False)
    age_group_counts_after = df_after['Age Group'].value_counts().sort_index()

    # Plotting the age groups
    plt.figure(figsize=(20, 10))

    plt.subplot(1,2,1)
    bars1 = age_group_counts_before.plot(kind='bar')
    plt.title('Completion Count by Age Group Before Three Stories')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    anotate(bars1)

    plt.subplot(1,2,2)
    bars2 = age_group_counts_after.plot(kind='bar')
    plt.title('Completion Count by Age Group After Three Stories')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    anotate(bars2)

    plt.suptitle(title,fontsize=25)

    plt.savefig('../charts/age_group_analysis.jpg')

    plt.show()

# A pie chart analysis for the age
def age_pie_chart_analysis(title):

    df_before = pd.read_csv(f'../synthesized_data/before/survey_data_success_before.csv')
    df_after = pd.read_csv(f'../synthesized_data/after/survey_data_success_after.csv')

    # Creating age groups
    bins = [18,35, 45, 55, 65, float('inf')]
    labels = ['18-34', '35-44', '45-54', '55-64', '65+']
    df_before['Age Group'] = pd.cut(df_before['Age'], bins=bins, labels=labels, right=False)
    age_group_counts_before = df_before['Age Group'].value_counts().sort_index()

    # Creating age groups
    df_after['Age Group'] = pd.cut(df_after['Age'], bins=bins, labels=labels, right=False)
    age_group_counts_after = df_after['Age Group'].value_counts().sort_index()

    # Plotting the age groups
    plt.figure(figsize=(20, 10))

    plt.subplot(1,2,1)
    colors = ['#32a89d', '#ff6b6b', '#ffc658', '#0a3d62', '#9b59b6','#9b59b6']
    age_group_counts_before.plot(kind='pie', autopct='%1.2f%%', startangle=140, colors=colors)
    plt.title('Before')
    plt.ylabel('')

    plt.subplot(1,2,2)
    age_group_counts_after.plot(kind='pie', autopct='%1.2f%%', startangle=140, colors=colors)
    plt.title('After')
    plt.ylabel('')

    plt.suptitle(title,fontsize=25)

    plt.savefig('../charts/age_group_analysis_2.jpg')

# Userwise analysis per day
def get_user_repetition_analysis(
        data,
        needed_number_of_repetition_for_analysis,
        title,
        data_frame = False
        ):
    
    if data_frame == False:
        df = read_excel_file(data)
    else:
        df = data
    df['Email'].value_counts()
    temp_data = pd.DataFrame(
            df['Email'].value_counts()
        )
    temp_data = temp_data.reset_index()
    temp_data = temp_data[temp_data['count'] >= needed_number_of_repetition_for_analysis]
    # Plotting
    # Create a scatter plot using Plotly Express
    fig = px.scatter(temp_data[:10], x=[1]*len(temp_data[:10]), y='Email', size='count', 
                    color='count', hover_name='Email', 
                    size_max=60, title=title)

    # Hide x-axis
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False})

    # Show the plot
    fig.show()

    return temp_data

def week_analysis(range_of_dates,week,number_of_repetition,month):

    if month == 'april_2024':
        year_and_month = '2024-04'
    else:
        year_and_month = '2023-09'

    data_frames = []
    for i in range_of_dates:
        if i < 10:
            date = '0'+ str(i)
        else:
            date = i
        survey_data = read_excel_file(f'../data/{month}/SurveyTakers_{year_and_month}-{date}.xls')
        survey_data.drop_duplicates(subset=['Email'], keep='first', inplace=True)
        data_frames.append(survey_data)

    week_data = pd.concat(data_frames,axis = 0)
    df = get_user_repetition_analysis(week_data,
                                            number_of_repetition,
                                            title =f'Users that came more than 3 times for the {week} week',
                                            data_frame=True)
    
    return df

# A function to see users that repeated in a month
def monthly_analysis(number_of_repetition,month):

    if month == 'april_2024':
        year_and_month = '2024-04'
    else:
        year_and_month = '2023-09'

    data_frames = []
    for i in range(1,30):
        if i < 10:
            date = '0'+ str(i)
        else:
            date = i

        if date == 24 and month != 'april_2024':
            data_path = f'../data/{month}/SurveyTakers_{year_and_month}-{date}.csv'
            survey_data = pd.read_csv(data_path)
        else:
            data_path = f'../data/{month}/SurveyTakers_{year_and_month}-{date}.xls'
            survey_data = read_excel_file(data_path)
        survey_data.drop_duplicates(subset=['Email'], keep='first', inplace=True)
        data_frames.append(survey_data)

    monthly_data = pd.concat(data_frames,axis = 0)
    df = get_user_repetition_analysis(monthly_data,
                                            number_of_repetition,
                                            title =f'Users that came more than {number_of_repetition} times in April',
                                            data_frame=True)
    
    return df

# Getting the total monthly data
def get_monthly_data(month):

    if month == 'april_2024':
        year_and_month = '2024-04'
    else:
        year_and_month = '2023-09'

    data_frames = []
    for i in range(1,30):
        if i < 10:
            date = '0'+ str(i)
        else:
            date = i
        
        if date == 24 and month != 'april_2024':
            data_path = f'../data/{month}/SurveyTakers_{year_and_month}-{date}.csv'
            survey_data = pd.read_csv(data_path)
        else:
            data_path = f'../data/{month}/SurveyTakers_{year_and_month}-{date}.xls'
            survey_data = read_excel_file(data_path)
        survey_data.drop_duplicates(subset=['Email'], keep='first', inplace=True)
        data_frames.append(survey_data)

    data = pd.concat(
        data_frames,
        axis = 0
    )

    return data

# Getting the exact date the user has repeated after six months
def get_exact_date_the_user_repeated(user_email):

    april_dates = []
    september_dates = []

    for i in range(1,30):
        if i < 10:
                date = '0'+ str(i)
        else:
            date = i
        survey_data = read_excel_file(f'../data/april_2024/SurveyTakers_2024-04-{date}.xls')
        if len(survey_data[survey_data['Email'] == user_email]) != 0:
            april_dates.append(date)

    for i in range(1,30):
        if i < 10:
                date = '0'+ str(i)
        else:
            date = i
        if i != 24:
            survey_data = read_excel_file(f'../data/september_2023/SurveyTakers_2023-09-{date}.xls')
        if len(survey_data[survey_data['Email'] == user_email]) != 0:
            september_dates.append(date)

    print(f'The user having email address of `{user_email}` was present on September:')
    for date in september_dates:
        print(date)
    print(f'And also after six months on September:')
    for date in april_dates:
        print(date)

# Refining the survey data
def refine_data(df):

    # Changing all the country codes by full state name
    df['State'] = df['State'].apply(get_country_name)

    # Remove spaces on the state data
    df['State'].fillna(df['State'].mode()[0],inplace = True)
    df['State'] = df['State'].apply(lambda state:state.replace(' ',''))

    # Remove spaces on the city data
    df['City'].fillna(df['City'].mode()[0],inplace = True)
    df['City'] = df['City'].apply(lambda city:city.replace(' ',''))

    # Let us take the columns that will be usefull for us
    columns_to_be_dropped = [
        'ID',
        'Affiliate ID',
        'Revenue Tracker ID',
        'Address1',
        'Address2',
        'Phone',
        'S3',
        'S4',
        'S5',
        'Response',
        'IP Address',
        'All Inbox Status',
        'Zip',
        'Source URL'
    ]
    usefull_columns = []
    for column in list(df.columns):
        if column not in columns_to_be_dropped:
            usefull_columns.append(column)

    df = df[usefull_columns]

    # Let us concatenate the first and last name into full name
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
    df['First Name'] = df['Full Name']
    df.drop(columns=['Last Name','Full Name'], inplace=True)
    df.rename(columns={'First Name': 'Full Name'}, inplace=True)

    # Getting only the time of created at and updated at column
    df['Created At'] = df['Created At'].apply(lambda x:x.split(' ')[1].split(':')[0])
    df['Updated At'] = df['Updated At'].apply(lambda x:x.split(' ')[1].split(':')[0])

    # Let us change the birth date column by age
    df['Birthdate'] = df['Birthdate'].apply(calculate_age)
    df.rename(columns={'Birthdate': 'Age'}, inplace=True)

    return df

# A function for automatic visualization
def auto_viz(df,save_fig_title):

    # Getting the general visualization for repeting users
    profile = ProfileReport(
        df,
        explorative = True
    )
    
    profile.to_file(f'../visualizations/{save_fig_title}.html')

# A function to see the overall analysis of the daily repeating users
def generate_report_of_repeting_users(survey_data_path,number_of_repetition,title,save_fig_title,data_frame=False):

    # Let us see users that repeat multiple times
    df = get_user_repetition_analysis(survey_data_path,
                                    number_of_repetition,
                                    title,
                                    data_frame=data_frame)

    repetedly_coming_users = list(df['Email'].values)
    # Getting the repeting users dataframe
    if data_frame == False:
        data = read_excel_file(survey_data_path)
    else:
        data = survey_data_path

    repeting_users_df = data[data['Email'].isin(repetedly_coming_users)]
    repeting_users_df.drop_duplicates(subset=['Email'], keep='first', inplace=True)

    repeting_users_df = refine_data(repeting_users_df)

    auto_viz(repeting_users_df,save_fig_title)

    return repeting_users_df

# Weekly report generation
def generater_report_of_repeting_users_for_week(range_of_dates,number_of_repetition,title,save_fig_title):

    data_frames = []
    for i in range_of_dates:
        if i < 10:
            date = '0'+ str(i)
        else:
            date = i
        survey_data = read_excel_file(f'../data/april_2024/SurveyTakers_2024-04-{date}.xls')
        survey_data.drop_duplicates(subset=['Email'], keep='first', inplace=True)
        data_frames.append(survey_data)

    week_data = pd.concat(data_frames,axis = 0)

    df = generate_report_of_repeting_users(week_data,number_of_repetition,title,save_fig_title,data_frame=True)

    return df

