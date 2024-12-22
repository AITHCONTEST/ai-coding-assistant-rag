import json
import logging
import os

import requests
import openai
import streamlit as st

SERVER_ADDR = os.getenv("SERVER_ADDR", "0.0.0.0:8000")
URL = f"http://{SERVER_ADDR}/v1/chat/completions"


@st.cache_data()
def create_gpt_completion(ai_model: str, messages: list[tuple[str, str]]) -> dict:
    try:
        openai.api_key = st.secrets.api_credentials.api_key
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    logging.info(f"{messages=}")
    header = {"Content-Type": "application/json"}
    data = {
        "model": ai_model,
        "messages": messages,
    }
    data = json.dumps(data)
    completion = requests.post(URL, headers=header, data=data)
    logging.info(f"{completion=}")
    return completion.json()
