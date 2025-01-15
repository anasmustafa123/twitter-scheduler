import streamlit as st
from datetime import date, time
import boto3
from boto3.dynamodb.conditions import Attr, Key
import requests
import json 
import sqlite3

st.title("Twitter Post Scheduler")


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("credentials.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            api_key TEXT,
            api_secret TEXT,
            access_token TEXT,
            access_secret TEXT,
            bearer_key TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add new user to the database
def add_user_to_db(username, api_key, api_secret, access_token, access_secret, bearer_key):
    conn = sqlite3.connect("credentials.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, api_key, api_secret, access_token, access_secret, bearer_key)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, api_key, api_secret, access_token, access_secret, bearer_key))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists!")
    conn.close()

# Fetch all users from the database
def get_all_users():
    conn = sqlite3.connect("credentials.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# Fetch user credentials by username
def get_user_credentials(username):
    conn = sqlite3.connect("credentials.db")
    c = conn.cursor()
    c.execute("""
        SELECT api_key, api_secret, access_token, access_secret, bearer_key
        FROM users WHERE username = ?
    """, (username,))
    user = c.fetchone()
    conn.close()
    return user

# Initialize database
init_db()



def dynamodb_insert(tweet_id, tweet_link, hashtags, tweet_schedule_day, tweet_schedule_hour, table):
    response = table.put_item(
    Item={
        "tweet_id": tweet_id,
        "tweet_link":tweet_link, 
        "hashtags":hashtags,
        "tweet_schedule_date": f"{tweet_schedule_day} {tweet_schedule_hour}",
    })
    print(f"Insert response {response}")


# Dropdown to select user
users = get_all_users()
selected_user = st.selectbox("Select User", [""] + users)


# Initialize session state for inputs
if 'tweet_link' not in st.session_state:
    st.session_state['tweet_link'] = ''
if 'hashtags' not in st.session_state:
    st.session_state['hashtags'] = ""
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = 'esWv9HtSbE874gTseBsxb1dfA'
if 'api_secret' not in st.session_state:
    st.session_state['api_secret'] = 'PsVZUysJjWUsNDQ31LclVIO3bYJ1Wl1ghMLdB3AMMTiT7K2dTV'
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = '1878485802734555137-tZdRehX55WfjkoIqUHS4mn4NOEWaBc'
if 'access_secret' not in st.session_state:
    st.session_state['access_secret'] = '7H0mkbgtusBaOlC3aFEZL4uFUtpnJZDL0LpdZaqJLvr0Q'
if 'bearer_key' not in st.session_state:
    st.session_state['bearer_key'] = r"AAAAAAAAAAAAAAAAAAAAAKFvyAEAAAAAXLyTrslica3p3hP3B%2FFjWTZPFiA%3DujZkrYuO6IyhoKWDqppoe5aNBQnRn0JNQqcKEcusvUTStRQBGA"
if 'schedule_day' not in st.session_state:
    st.session_state['schedule_day'] = date(2025, 1, 3)  # Default as datetime.date
if 'schedule_hour' not in st.session_state:
    st.session_state['schedule_hour'] = time(4, 10)  # Default as datetime.time


if selected_user:
    user_credentials = get_user_credentials(selected_user)
    print(f"user the user_credentials {user_credentials}")
    if user_credentials:
        st.session_state['api_key'] =  user_credentials[0]
        st.session_state['api_secret']=  user_credentials[1]
        st.session_state['access_token']=  user_credentials[2]
        st.session_state['access_secret']=  user_credentials[3]
        st.session_state['bearer_key'] =   user_credentials[4]
        st.success(f"Loaded credentials for {selected_user}")


# Input fields
tweet_link = st.text_input("Twitter Post Link", value=st.session_state['tweet_link'], key="tweet_link")
hashtags = st.text_area("Add Hashtags (comma-separated)", value=st.session_state['hashtags'], key="hashtags")
api_key = st.text_input("API Key", value=st.session_state['api_key'], key="api_key")
api_secret = st.text_input("API Secret", type="password", value=st.session_state['api_secret'], key="api_secret")
access_token = st.text_input("Access Token", value=st.session_state['access_token'], key="access_token")
access_secret = st.text_input("Access Token Secret", type="password", value=st.session_state['access_secret'], key="access_secret")
bearer_key = st.text_input("Bearer Key", type="password", value=st.session_state['bearer_key'], key="bearer_key")
schedule_day = st.date_input("Schedule date", value=st.session_state['schedule_day'], key="schedule_day")
schedule_hour = st.time_input("Schedule Time", value=st.session_state['schedule_hour'], key="schedule_hour")



#-----------------------------------

# Handle buttons
col1, col2 = st.columns(2)

def schedule_post():
    try:
        # Convert date and time to strings for storage
        schedule_day_str = schedule_day.isoformat()
        schedule_hour_str = schedule_hour.isoformat()
                
        load = {
            "body": {
                "tweet_link": tweet_link, 
                "hashtags": hashtags,
               "schedule_day": schedule_day_str,
                "schedule_hour": schedule_hour_str,
                "api_key": api_key,
                "api_secret": api_secret,
                "access_token" : access_token,
                "access_secret": access_secret,
                "bearer_key": bearer_key
            }
        }
        response = requests.post("https://zspemvvgs2.execute-api.us-east-1.amazonaws.com/default/schedule_tweet", headers={"Content-Type": "application/json"}, data=json.dumps(load))
        st.success(f"Tweet with link {tweet_link} scheduled successfully! on {schedule_day_str}{schedule_hour_str}  ---> {response.status_code}")
    except Exception as e:
        st.error(f"Error scheduling tweet: {e}")

def clear_states():
    # Clear all session state inputs
    st.session_state['tweet_link'] = ""
    st.session_state['hashtags'] = ""
    st.session_state['api_key'] = ""
    st.session_state['api_secret'] = ""
    st.session_state['access_token'] = ""
    st.session_state['access_secret'] = ""
    st.session_state['bearer_key'] = ""
    st.session_state['schedule_day'] = date.today()  # Reset to today's date
    st.session_state['schedule_hour'] = time(0, 0)  # Reset to midnight

with col1:
    st.button("Schedule Post", on_click=schedule_post)

with col2:
    st.button("Clear", on_click=clear_states)


#-----------------------------------


# Add new user section
st.subheader("Add New User")
username = st.text_input("Username")
new_api_key = st.text_input("New API Key")
new_api_secret = st.text_input("New API Secret", type="password")
new_access_token = st.text_input("New Access Token")
new_access_secret = st.text_input("New Access Token Secret", type="password")
new_bearer_key = st.text_input("New Bearer Key", type="password")



if st.button("Add New User"):
    if username and new_api_key and new_api_secret and new_access_token and new_access_secret and new_bearer_key:
        add_user_to_db(username, new_api_key, new_api_secret, new_access_token, new_access_secret, new_bearer_key)
        st.success(f"User {username} added successfully!")
    else:
        st.error("All fields are required to add a new user!")
