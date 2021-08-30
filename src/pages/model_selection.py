from typing import List
from typing import Optional

import streamlit as st

from src.stores import AppStateKeys
from src.stores.app_state import AppState
from src.stores.app_state import MAX_ALLOWED_MODELS
from src.utils.models_query import DownloadableModel
from src.utils.models_query import DownloadableModelsState
from src.utils.models_query import HUGGINGFACE_BASE_URL


@st.cache
def cached_download_model_page(
        page_i: Optional[int] = None,
        search: Optional[str] = None,
        other: Optional[str] = None,
) -> List[DownloadableModel]:
    return DownloadableModelsState.download_model_page(page_i, search, other)


def render():
    if len(AppState().get_by_key(AppStateKeys.selected_models)) > 0:
        st.title('Selected Models')
        cols = st.columns([0.1, 0.8])
        for model_name in AppState().get_by_key(AppStateKeys.selected_models):
            with cols[0]:
                st.button(
                    label='Deselect', key=model_name,
                    on_click=AppState().deselected_model, args=[model_name]
                )
            with cols[1]:
                st.markdown(model_name)

        st.markdown('___')

    selected_task = AppState().get_by_key(AppStateKeys.selected_task)
    filter_cols = st.columns(2)
    with filter_cols[0]:
        name_filter = st.text_input('Filter By Name')
    with filter_cols[1]:
        page_num = st.number_input('Page number', min_value=0, step=1)

    filtered_models = cached_download_model_page(
        other=selected_task,
        search=name_filter,
        page_i=page_num
    )

    st.markdown('___')

    model_arg_names = list(DownloadableModel.__init__.__annotations__.keys())[:-1]
    cols = st.columns(len(model_arg_names) + 1)
    for i, title in enumerate(model_arg_names):
        with cols[i + 1]:
            st.markdown(str.title(title.replace('_', ' ')))

    st.markdown('___')

    for model_i, model in enumerate(filtered_models):
        if model_i > 50:
            continue
        cols = st.columns(len(model_arg_names) + 1)
        for i, arg_name in enumerate(model_arg_names):
            with cols[i + 1]:
                val = getattr(model, arg_name)
                if arg_name == 'model_name':
                    val = f"[{val}]({HUGGINGFACE_BASE_URL}{val})"
                if val is not None:
                    st.markdown(val)
        with cols[0]:
            if (
                    len(AppState().get_by_key(AppStateKeys.selected_models)) < MAX_ALLOWED_MODELS
                    and (model.model_name not in AppState().get_by_key(AppStateKeys.selected_models))
            ):
                st.button('Select', key=model.model_name, on_click=AppState().select_model, args=[model.model_name])
