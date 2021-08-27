import streamlit as st
from typing import TypeVar

T = TypeVar('T')


def _init_field(field_name: str, value: T) -> T:
    if field_name not in st.session_state:
        st.session_state[field_name] = value

    return st.session_state[field_name]
