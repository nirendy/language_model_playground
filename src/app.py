import streamlit as st
from src.consts.locale import Locale
from src.components.model_playground import run

if __name__ == "__main__":
    st.set_page_config(
        page_title=Locale.app_title, page_icon=":memo:"
    )

    run()
