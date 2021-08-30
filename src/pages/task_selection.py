import streamlit as st
from transformers.modelcard import TASK_TAG_TO_NAME_MAPPING

import src.pages.demo as demo
from src.stores import AppStateKeys
from src.stores import Pages
from src.stores.app_state import AppState
from src.stores.app_state import MAX_ALLOWED_MODELS
from src.utils.models_query import DownloadableModel
from src.utils.models_query import DownloadableModelsState


def render():
    AppState.get_or_create_by_key(AppStateKeys.selected_task, 'text-generation')

    st.radio(
        'Available Tasks',
        options=TASK_TAG_TO_NAME_MAPPING.keys(),
        format_func=lambda x: TASK_TAG_TO_NAME_MAPPING[x],
        key=AppStateKeys.selected_task.name
    )
