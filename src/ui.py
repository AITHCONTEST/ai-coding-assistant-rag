from streamlit_option_menu import option_menu
from streamlit_utils.lang import en
from streamlit_utils.conversation import (
    show_chat_buttons,
    show_text_input,
    show_conversation,
)
import streamlit as st
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


PAGE_TITLE: str = "AI Code Assistant"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
AI_MODEL_OPTIONS: list[str] = [
    "ChatGPT 4o",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

selected_lang = option_menu(
    menu_title=None,
    options=[LANG_EN],
    icons=["globe2", "translate"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""


def main() -> None:
    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    show_text_input()
    show_chat_buttons()


if __name__ == "__main__":
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case _:
            st.session_state.locale = en
    st.markdown(
        f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>",
        unsafe_allow_html=True,
    )
    main()
