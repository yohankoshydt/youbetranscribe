import streamlit as st
import requests
import httpx
import urllib.request
import json

# Streamlit App Title
st.title("API Call Test in Streamlit")

# API URL for testing
url = "https://api.publicapis.org/entries"

# Function to call API using requests
def call_api_requests():
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["entries"][:3]
        return f"Failed with status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return str(e)

# Function to call API using httpx
def call_api_httpx():
    try:
        response = httpx.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["entries"][:3]
        return f"Failed with status code {response.status_code}"
    except httpx.RequestError as e:
        return str(e)

# Function to call API using urllib
def call_api_urllib():
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
            return data["entries"][:3]
    except Exception as e:
        return str(e)

# Dropdown to select API method
method = st.selectbox("Select API Method", ["requests", "httpx", "urllib"])

# Button to make the API call
if st.button("Test API Call"):
    if method == "requests":
        result = call_api_requests()
    elif method == "httpx":
        result = call_api_httpx()
    elif method == "urllib":
        result = call_api_urllib()
    
    # Display Result
    if isinstance(result, list):
        st.success("API Call Successful ✅")
        st.json(result)
    else:
        st.error(f"API Call Failed: {result}")
