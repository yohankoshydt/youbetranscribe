import streamlit as st
import requests

# Streamlit app title
st.title("API Call Test in Streamlit")

# API URL
url = "https://api.publicapis.org/entries"  # Public API for testing

# Button to trigger API request
if st.button("Test API Call"):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            st.success("API call successful! ✅")
            data = response.json()
            st.write("Sample Response:")
            st.json(data["entries"][:3])  # Show first 3 entries
        else:
            st.error(f"API call failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
