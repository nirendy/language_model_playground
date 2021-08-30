import streamlit as st

from src.components.text_with_predefined import select_input_text
from src.stores.app_state import AppState
from src.stores.model_state import ModelState
from src.stores import AppStateKeys
from src.consts.locale import Locale
import src.consts.presets as Presets
import src.pages.auto_model_causal_lm as auto_model_causal_lm


# endregion

def render():
    with st.container():
        select_input_text(
            key=AppStateKeys.init_input_tokens.name,
            label=Locale.init_sentence,
            options=Presets.INPUT_TOKENS,
            use_text_area=True
        )

    st.sidebar.write('___')

    if not AppState.get_init_input_tokens():
        st.warning('Empty initial sentence')
        st.stop()

    active_models_states = ModelState.get_active_model_states()
    auto_model_causal_lm.render(active_models_states)
