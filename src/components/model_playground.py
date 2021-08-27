import streamlit as st

import src.components.generation_params_selector as GenerationParamsSelector
from src.components.text_with_predefined import select_input_text
from src.stores.app_state import AppState
from src.stores.model_state import available_models
from src.stores.model_state import ModelState
from src.stores import ModelStateKeys
from src.consts.locale import Locale
import src.consts.presets as Presets
import src.components.auto_model_causal_lm as auto_model_causal_lm
import streamlit_tags as st_tags


# endregion

def run():
    AppState.init_state()

    with st.container():
        select_input_text(
            key=ModelStateKeys.init_input_tokens.name,
            label=Locale.init_sentence,
            options=Presets.INPUT_TOKENS,
            use_text_area=True
        )

    st_tags.st_tags_sidebar(
        label=Locale.models_selection_label,
        value=AppState.selected_models(),
        text=Locale.models_selection_tooltip,
        suggestions=available_models,
        maxtags=2,
        key=ModelStateKeys.selected_models.name,
    )

    st.sidebar.write('___')

    with st.sidebar.container():
        GenerationParamsSelector.run()

    active_models_states = ModelState.get_active_model_states()

    if len(active_models_states) == 0:
        st.warning('No models loaded')
        st.stop()

    if not AppState.get_init_input_tokens():
        st.warning('Empty initial sentence')
        st.stop()

    st.write([model_state.model_name for model_state in active_models_states])
    auto_model_causal_lm.render(active_models_states)
