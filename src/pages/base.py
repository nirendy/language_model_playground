import streamlit as st

import src.pages.home as home
import src.pages.model_selection as model_selection
import src.pages.task_selection as task_selection
import src.pages.generation_params_tuning as generation_params_tuning
import src.pages.demo as demo
from src.stores import AppStateKeys
from src.stores import Pages
from src.stores.app_state import AppState


def render_page_button(page: Pages):
    selected_page = AppState().get_or_create_by_key(AppStateKeys.selected_page, Pages.home)
    st.button(page.value, on_click=AppState().set_by_key, args=(AppStateKeys.selected_page, page))
    if selected_page.name == page.name:
        st.write('___')


def render_progress_content(is_sidebar=False):
    cols = None
    col_i = 0

    if not is_sidebar:
        cols = st.columns(len(Pages) * 3)
        with cols[col_i + 1]:
            render_page_button(Pages.home)

        col_i += 3
        with cols[col_i + 1]:
            render_page_button(Pages.task_selection)

    if not AppState().is_inited_by_key(AppStateKeys.selected_task):
        return

    if is_sidebar:
        st.write(AppState().get_by_key(AppStateKeys.selected_task))
    else:
        col_i += 3
        with cols[col_i + 1]:
            render_page_button(Pages.model_selection)

    if not AppState().is_model_selected:
        return

    if is_sidebar:
        st.write(AppState().get_by_key(AppStateKeys.selected_models))
        # if len(AppState().selected_models()) > 0:
        #     for model_name in AppState().selected_models():
        #         st.button(
        #             label=f'Deselect {model_name}',
        #             on_click=AppState().deselected_model, args=[model_name]
        #         )
    else:
        col_i += 3
        with cols[col_i + 1]:
            render_page_button(Pages.generation_params_tuning)

    if is_sidebar:
        generation_inputs = AppState().get_generation_inputs()
        with st.expander('Generation Inputs:', expanded=True):
            st.write(generation_inputs)
        debugging_params = AppState().get_debugging_params()
        with st.expander('Debugging Params:', expanded=True):
            st.write(debugging_params)
    else:
        col_i += 3
        with cols[col_i + 1]:
            render_page_button(Pages.demo)


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
