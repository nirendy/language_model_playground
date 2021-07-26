import streamlit as st
from src.components.text_with_predefined import select_input_text
from src.consts.app_state import ModelState
from src.consts.app_state import available_models
from src.utils.model import Model, loading_model


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
