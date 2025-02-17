import requests
import streamlit as st

data = requests.get("'https://jsonplaceholder.typicode.com/todos/1'").json()

st.write(data)
