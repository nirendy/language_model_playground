from typing import List

import streamlit as st
import pandas as pd
import torch

from src.stores.app_state import AppState
from src.stores.model_state import ModelState
from src.stores.model_state import compute_input_ids
from src.utils.logits import TokenizerDebugger
from src.stores.model_state import generate_model_output


def render2(models_states):
    cols = st.columns(len(models_states))
    for i, model_state in enumerate(models_states):
        with cols[i]:
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

            if model_state.is_loaded():
                input_ids = compute_input_ids(model_state.get_tokenizer(), AppState.get_init_input_tokens())
                torch.manual_seed(AppState.get_generation_seed())

                # initial
                model_outputs = model_state.get_model().generate(
                    input_ids=input_ids,
                    **AppState.get_generation_inputs()
                )

                tokenizer_debugger = TokenizerDebugger(model_state.get_tokenizer())
                for i, model_output in enumerate(model_outputs):
                    if i > 0:
                        st.write('___')

                    st.text(model_state.get_tokenizer().decode(model_output, skip_special_tokens=True))

                    generated_model = model_state.get_model()(model_output)
                    res = tokenizer_debugger.get_sequence_logit_top_n_tokens(
                        model_output, generated_model.logits,
                        AppState.get_number_of_alternative_tokens()
                    )

                    st.dataframe(pd.DataFrame(res).fillna(''))


def render(models_states: List[ModelState]):
    def create_cols():
        return st.columns(len(models_states))

    model_titles_cols = create_cols()
    for i, model_state in enumerate(ModelState.get_active_model_states()):
        if model_state.should_show_load_button():
            model_state.load_model()
        with model_titles_cols[i]:
            if model_state.is_erroneous_name():
                st.write(f"Model named '{model_state.model_name}' was not found!")
            else:
                st.markdown(f"## **{model_state.model_name}**")

    model_outputs = [
        generate_model_output(model_state.model_name) if model_state.is_loaded() else None
        for model_state_i, model_state in enumerate(models_states)
    ]

    for output_i in range(AppState.get_num_return_sequences()):
        cols_sentence = create_cols()
        cols_debug = create_cols()
        for model_state_i, model_state in enumerate(models_states):
            if model_state.is_loaded():
                model_output = model_outputs[model_state_i][output_i]
                tokenizer_debugger = TokenizerDebugger(model_state.get_tokenizer())

                with cols_sentence[model_state_i]:
                    st.write(model_state.get_tokenizer().decode(model_output, skip_special_tokens=True))
                with cols_debug[model_state_i]:
                    generated_model = model_state.get_model()(model_output)
                    res = tokenizer_debugger.get_sequence_logit_top_n_tokens(
                        model_output, generated_model.logits,
                        AppState.get_number_of_alternative_tokens()
                    )

                    st.dataframe(pd.DataFrame(res).fillna(''))
