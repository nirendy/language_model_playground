import streamlit as st

import src.pages.home as home
import src.pages.model_selection as model_selection
import src.pages.demo as demo
from src.stores import AppStateKeys
from src.stores import Pages
from src.stores.app_state import AppState


def render():
    AppState().init_state()
    selected_page = AppState().get_or_create_by_key(AppStateKeys.selected_page, Pages.home)

    with st.sidebar:
        if selected_page.name != Pages.home.name:
            cols = st.columns(2)
            cols[0].button(
                Pages.home.value,
                on_click=AppState().set_by_key,
                args=(AppStateKeys.selected_page, Pages.home)
            )
            if AppState().is_model_selected and (selected_page.name != Pages.demo.name):
                cols[1].button(
                    Pages.demo.value,
                    on_click=AppState().set_by_key,
                    args=(AppStateKeys.selected_page, Pages.demo)
                )
            elif selected_page.name != Pages.model_selection.name:
                cols[1].button(
                    Pages.model_selection.value,
                    on_click=AppState().set_by_key,
                    args=(AppStateKeys.selected_page, Pages.model_selection)
                )

    if selected_page.name == Pages.home.name:
        home.render()
    if selected_page.name == Pages.model_selection.name:
        model_selection.render()
    if selected_page.name == Pages.demo.name:
        demo.render()
