import json
import logging
from typing import List  # NOQA: UP035

import requests
import openai
import streamlit as st

URL = "http://127.0.0.1:7777/chat/completions"

@st.cache_data()
def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
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
    # return completion.json()['output']
    return completion.json()
