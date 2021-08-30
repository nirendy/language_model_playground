import streamlit as st
from typing import TypeVar

T = TypeVar('T')


def _is_inited(field_name) -> bool:
    return field_name in st.session_state


def _init_field(field_name: str, value: T) -> T:
    if not _is_inited(field_name):
        st.session_state[field_name] = value

    return st.session_state[field_name]
