from typing import get_type_hints

import streamlit as st
import tokenizers
import torch

import src.components.model_selector as ModelSelector
from src.app_state import Inputs
from src.components.text_with_predefined import select_input_text
from src.consts.locale import Locale
import src.consts.presets as Presets
from src.utils.logits import TokenizerDebugger
import src.components.auto_model_causal_lm as auto_model_causal_lm


# region Functions

@st.cache(hash_funcs={tokenizers.Tokenizer: id})
def compute_input_ids(tokenizer, input_sentence):
    return tokenizer.encode(input_sentence, return_tensors='pt')


# endregion


def select_generation_params():
    def set_chosen_generation_preset():
        if st.session_state['chosen_generation_preset'] != Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]:
            for k, v in Presets.TOKEN_GENERATION_CONFIGURATION[st.session_state['chosen_generation_preset']].items():
                st.session_state[k] = v
        # else:
        #     for key in get_type_hints(Inputs):
        #         del st.session_state[key]

    st.sidebar.selectbox(
        'Generation Preset:',
        options=Presets.TOKEN_GENERATION_CONFIGURATION_KEYS,
        key='chosen_generation_preset',
        on_change=set_chosen_generation_preset
    )

    def changed(t):
        # print(f"{t} changed {st.session_state[t]}")
        pass

    # print(list(st.session_state.keys()))
    for k, k_type in get_type_hints(Inputs).items():
        label = k

        if k not in st.session_state:
            # print(f'init {k}')
            st.session_state[k] = getattr(Inputs, k)

        if st.session_state['chosen_generation_preset'] == Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]:
            # st.sidebar.write(f"{k}: {st.session_state[k]}, {getattr(Inputs, k)}")
            pass
        elif k not in Presets.TOKEN_GENERATION_CONFIGURATION[st.session_state['chosen_generation_preset']]:
            label += ' (ignored)'

        if k_type == str:
            st.sidebar.text_input(
                label=label,
                key=k,
                on_change=changed,
                args=[k]
            )
        elif k_type == int:
            st.sidebar.number_input(
                label=label,
                key=k,
                min_value=0,
                on_change=changed,
                args=[k]
            )
        elif k_type == bool:
            st.sidebar.checkbox(
                label=label,
                key=k,
                on_change=changed,
                args=[k]
            )
        elif k_type == float:
            st.sidebar.number_input(
                label=label,
                key=k,
                min_value=0.0,
                on_change=changed,
                args=[k]
            )


def run():
    with st.sidebar.beta_container():
        if st.button('Clear Cache'):
            for key in st.session_state.keys():
                del st.session_state[key]

    st.sidebar.write('___')

    with st.sidebar.beta_container():
        ModelSelector.render()

    with st.beta_container():
        select_input_text(
            key='init_input_tokens',
            label=Locale.init_sentence,
            options=Presets.INPUT_TOKENS
        )

    st.sidebar.write('___')

    select_generation_params()

    st.sidebar.write('___')
    st.sidebar.write('Generation Inputs:')
    generation_inputs = {
        k: st.session_state[k]
        for k in get_type_hints(Inputs)
        if (
                st.session_state['chosen_generation_preset'] == Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]
                or
                (k in Presets.TOKEN_GENERATION_CONFIGURATION[st.session_state['chosen_generation_preset']])
        )
    }

    for k, v in generation_inputs.items():
        st.sidebar.write(f"{k}: {v}")

    if st.session_state['is_model_loaded']:
        input_ids = compute_input_ids(st.session_state['model'].tokenizer, st.session_state['init_input_tokens'])
        torch.manual_seed(st.session_state['seed'])

        # initial
        model_outputs = st.session_state['model'].model.generate(
            input_ids=input_ids,
            **generation_inputs
        )

        tokenizer_debugger = TokenizerDebugger(st.session_state['model'].tokenizer)
        auto_model_causal_lm.run(st.session_state['model'], model_outputs, tokenizer_debugger)
