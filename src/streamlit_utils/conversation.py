from random import randrange

import streamlit as st
from streamlit_chat import message

from .agi.chat_gpt import create_gpt_completion


def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10**8)
    st.session_state.costs = []
    st.session_state.total_tokens = []


def show_text_input() -> None:
    st.text_area(
        label=st.session_state.locale.chat_placeholder,
        value=st.session_state.user_text,
        key="user_text",
    )


def get_user_input():
    match st.session_state.input_kind:
        case st.session_state.locale.input_kind_1:
            show_text_input()
        case _:
            show_text_input()


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(
                st.session_state.past[i],
                is_user=True,
                key=str(i) + "_user",
            )
            message(st.session_state.generated[i], key=str(i))


def show_gpt_conversation() -> None:
    try:
        completion = create_gpt_completion("ChatGPT 4o", st.session_state.messages)
        ai_content = completion.get("content")
        st.session_state.messages.append(("assistant", ai_content))
        if ai_content:
            show_chat(ai_content, st.session_state.user_text)
    except Exception as e:
        st.error(e)


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append(("user", st.session_state.user_text))
    else:
        st.session_state.messages = [
            ("user", st.session_state.user_text),
        ]
    show_gpt_conversation()
