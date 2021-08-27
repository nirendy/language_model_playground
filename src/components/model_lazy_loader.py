import streamlit as st

from src.stores.model_state import ModelState


def render(model_state: ModelState):
    def load_model():
        model_state.load_model()

    if model_state.is_erroneous_name():
        st.write(f"Model named {model_state.model_name} was not found!")

    if model_state.should_show_load_button():
        st.button(
            label=f"Load {model_state.model_name}",
            key=model_state.model_name + '_load_button',
            on_click=load_model
        )
