import streamlit as st
import tokenizers
import torch

import src.components.model_selector as ModelSelector
import src.components.generation_params_selector as GenerationParamsSelector
from src.components.text_with_predefined import select_input_text
from src.components.text_with_predefined import select_input_text2
from src.consts.app_state import AppState
from src.consts.app_state import ModelStateKeys
from src.consts.locale import Locale
import src.consts.presets as Presets
from src.utils.logits import TokenizerDebugger
import src.components.auto_model_causal_lm as auto_model_causal_lm

import streamlit_tags as st_tags


# region Functions

@st.cache(hash_funcs={tokenizers.Tokenizer: id})
def compute_input_ids(tokenizer, input_sentence: str):
    return tokenizer.encode(input_sentence, return_tensors='pt')


# endregion

def run():
    AppState.init_state()

    with st.beta_container():
        select_input_text(
            key=ModelStateKeys.init_input_tokens.name,
            label=Locale.init_sentence,
            options=Presets.INPUT_TOKENS,
        )

    st_tags.st_tags_sidebar(
        label=Locale.models_selection_label,
        text=Locale.models_selection_tooltip,
        suggestions=ModelSelector.available_models,
        maxtags=2,
        key=ModelStateKeys.selected_models.name,
    )

    st.sidebar.write('___')
    with st.sidebar.beta_container():
        GenerationParamsSelector.run()

    active_models = AppState.get_active_model_states()

    if len(active_models) == 0:
        st.warning('No models loaded')
        st.stop()

    if not AppState.get_init_input_tokens():
        st.warning('Empty initial sentence')
        st.stop()

    st.write('___')
    cols = st.beta_columns(len(active_models))
    for i, model_state in enumerate(AppState.get_active_model_states()):
        with cols[i]:
            ModelSelector.render(model_state)

            if model_state.is_loaded():
                input_ids = compute_input_ids(model_state.get_tokenizer(), AppState.get_init_input_tokens())
                torch.manual_seed(AppState.get_generation_seed())

                # initial
                model_outputs = model_state.get_model().generate(
                    input_ids=input_ids,
                    **AppState.get_generation_inputs()
                )

                tokenizer_debugger = TokenizerDebugger(model_state.get_tokenizer())
                auto_model_causal_lm.render(model_state, model_outputs, tokenizer_debugger)
