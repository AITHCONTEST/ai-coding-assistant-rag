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
                seed=st.session_state.seed,
            )
            message("", key=str(i), seed=st.session_state.seed)
            st.markdown(st.session_state.generated[i])
            st.caption(
                f"""
                {st.session_state.locale.tokens_count}{st.session_state.total_tokens[i]} |
                {st.session_state.locale.message_cost}{st.session_state.costs[i]:.5f}$
            """,
                help=f"{st.session_state.locale.total_cost}{sum(st.session_state.costs):.5f}$",
            )


def show_gpt_conversation() -> None:
    try:
        completion = create_gpt_completion(
            st.session_state.model, st.session_state.messages
        )
        ai_content = completion.get("content")
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content, st.session_state.user_text)
    except Exception as e:
        st.error(e)


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append(
            {"role": "user", "content": st.session_state.user_text}
        )
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    show_gpt_conversation()
