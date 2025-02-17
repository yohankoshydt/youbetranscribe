import streamlit as st
import requests
import httpx
import urllib.request
import json

# Streamlit App Title
st.title("API Call Test in Streamlit")


import httpx

# API URL for testing
url = "https://fake-json-api.mock.beeceptor.com/users"

# Function to call API using requests
def call_api_requests():
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
                return response.json()
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



from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(youtube_url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def get_available_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = {t.language_code: t.language for t in transcript_list}
        return available_languages
    except Exception as e:
        st.error(f"Error fetching languages: {e}")
        return {}



import streamlit as st

def get_available_languages(video_id):
    # Dummy function to simulate language fetching
    return {"en": "English", "es": "Spanish"}

def main():
    st.title("YouTube Transcript Language Fetcher")
    
    video_id = "DJy4PV6kETM"
    
    # Fetch available languages
    available_languages = get_available_languages(video_id)
    
    # Display available languages
    if available_languages:
        st.subheader("Available Languages:")
        st.write(available_languages)
    else:
        st.error("No available languages found.")

if __name__ == "__main__":
    main()
