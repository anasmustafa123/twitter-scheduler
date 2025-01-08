import streamlit as st
from datetime import date, time
#import tweepy
#import boto3
#from boto3.dynamodb.conditions import Attr, Key
import requests
import json

st.title("Twitter Post Scheduler")

# Initialize session state for inputs
if 'tweet_link' not in st.session_state:
    st.session_state['tweet_link'] = ''
if 'hashtags' not in st.session_state:
    st.session_state['hashtags'] = ""
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = 'FKOE1jjwhZ6guE6wO8YlkuemL'
if 'api_secret' not in st.session_state:
    st.session_state['api_secret'] = 'AePsZOTt55vTnrB4J9bEakyyzPwfAc7Jn5g90UZdfAhAkLyAL9'
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = '1876576679839072256-mbmZ9QQzvIYzH2SJ8IjYahI6JmTcD3'
if 'access_secret' not in st.session_state:
    st.session_state['access_secret'] = 'sNYC8cFIB2NgEIE8JI6pI179GLV7D2BhjRwev9GOMjVRz'
if 'bearer_key' not in st.session_state:
    st.session_state['bearer_key'] = r"AAAAAAAAAAAAAAAAAAAAAAX2xwEAAAAAh4PoQtZKc2n9%2FS3yXxN8RTTPVyQ%3DPXcivYLSg7u8E711xGeL40XIq8fJFagHg5R5J7Bak24834x48U"
if 'schedule_day' not in st.session_state:
    st.session_state['schedule_day'] = date(2025, 1, 3)  # Default as datetime.date
if 'schedule_hour' not in st.session_state:
    st.session_state['schedule_hour'] = time(4, 10)  # Default as datetime.time

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

# Handle buttons
col1, col2 = st.columns(2)

def schedule_post():
    try:
        # Convert date and time to strings for storage
        schedule_day_str = schedule_day.isoformat()
        schedule_hour_str = schedule_hour.isoformat()
        
        payload = {
                "body": {
                    "tweet_link": "https://x.com/embersunn/status/1875598314663768282",
                    "api_key": "t7tVUjfLsfrZyiURbeurCroTo",
                    "api_secret_key": "r9adKisBC2L4BE8iK1puLMdc5zlgeLhtPbxaOcMQnneOiWWsne",
                    "access_token": "711948595856015363-0OuQzTItXfuEI1gD2Vc6MxE34K29c48",
                    "access_token_secret": "nPDqKN5fQ2GFZMf1cSPHS6GWvBqpfkuGgm2EADihoLoLi",
                    "Bearer_key": "AAAAAAAAAAAAAAAAAAAAAKJVxwEAAAAAC%2FmLXuFwsFlKjGYM8qs7y5LlSAY%3Da3tSSEQjEwSYegby4nMWdD3gfALbyZ39IT1qG6uGCxovKeLG8C",
                    "client_id": "c3FpcTdpU2NLTWhPUmFseDhvbWQ6MTpjaQ",
                    "client_secret": "R9cGwVd_JPCYUWE6NQ2xNJp7GEwveTkT7NVk1szZBEbEz58Pak",
                    "hashtags": "#new",
                    "schedule_day": "2025-01-06",
                    "schedule_hour": "22-20"
                }
            }
        
        shcedule_tweet_lambda = "https://0ay03k7zii.execute-api.us-east-1.amazonaws.com/default/shcedule_tweet"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(shcedule_tweet_lambda, headers=headers, data=json.dumps(payload))
        print({tweet_link, hashtags, api_key, api_secret, access_token, access_secret, bearer_key, schedule_day_str, schedule_hour_str})
        st.success(f"Tweet scheduled successfully! {response}")
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
