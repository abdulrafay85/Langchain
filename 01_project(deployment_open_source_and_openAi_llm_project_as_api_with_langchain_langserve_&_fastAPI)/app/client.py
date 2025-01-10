import streamlit as st
import requests

def get_open_ai_respose(input_text):
    response= requests.post(
        "http://localhost:8000/essay/invoke",
        json={"input": {"topic": input_text}}
    )
    response.json()['output']['content']

## streamlit framwork
st.title("My First Streamlit App")
input_text = st.text_input("Write an essay on")


if input_text:
    st.write(get_open_ai_respose(input_text))