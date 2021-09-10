import streamlit as st

from src.stores import AppStateKeys
from src.stores import Pages
from src.stores.app_state import AppState


def render():
    selected_model = AppState().get_by_key(AppStateKeys.selected_models)
    selected_model_text = ''
    if len(selected_model) > 0:
        selected_model_text = f" ({selected_model[0]} is selected)"

    st.write(
        f"""
        # Welcome to the Transformers Playground!
        
        This playground designed as an interactive tutorial for the Transformers library by HuggingFace 🤗 
        
        It will be done in steps, tha every step is relying on the one before it
        
        Now you're in the Home step, you can move steps clicking on the corresponding button
        
        ---
        **Step 1: Choose a model{selected_model_text}**
        - Models designed or trained for a specific task, therefore, we want to browse only models that are trained 
        for the selected task
        """
    )
    st.button(
        Pages.model_selection.value,
        on_click=AppState().set_by_key,
        args=(AppStateKeys.selected_page, Pages.model_selection)
    )
    st.write('___')

    if len(selected_model) > 0:
        st.button(
            Pages.demo.value,
            on_click=AppState().set_by_key,
            args=(AppStateKeys.selected_page, Pages.demo)
        )
        st.write('___')

    st.write(
        f"""
        **Step 3: Choose Generation Params**
        - There are degrees of freedom in deciding how to create the resulted output by the logits...

        **Step 4: See and compare the results**
        - See multiple models output simultaneously and notice the difference in the results
        
        ---
        
        Start by clicking on the Task Selection Button at the top. 
        You can return this page for reference at any point!
        """
    )
