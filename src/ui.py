from streamlit_option_menu import option_menu
from src.streamlit.lang import en
from src.streamlit.conversation import (
    show_chat_buttons,
    show_text_input,
    show_conversation,
)
import streamlit as st

PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
AI_MODEL_OPTIONS: list[str] = [
    "microsoft/Phi-3.5-mini-instruct",
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
    c1, c2 = st.columns(2)
    with c1, c2:
        c1.selectbox(
            label=st.session_state.locale.select_placeholder1,
            key="model",
            options=AI_MODEL_OPTIONS,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(
                st.session_state.locale.radio_text1,
                st.session_state.locale.radio_text2,
            ),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                c2.selectbox(
                    label=st.session_state.locale.select_placeholder2,
                    key="role",
                    options=st.session_state.locale.ai_role_options,
                )
            case st.session_state.locale.radio_text2:
                c2.text_input(
                    label=st.session_state.locale.select_placeholder3, key="role"
                )
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
