import streamlit as st
from typing import get_type_hints

from src.consts import presets as Presets
from src.consts.app_state import DebuggingParamsDefaults
from src.consts.app_state import GenerationInputDefaults, AppState
from src.consts.app_state import ModelStateKeys
from src.consts.locale import Locale


def select_generation_params():
    st.selectbox(
        Locale.generation_preset_selectbox_label,
        options=Presets.TOKEN_GENERATION_CONFIGURATION_KEYS,
        key=ModelStateKeys.chosen_generation_preset.name,
        on_change=AppState.set_chosen_generation_preset
    )

    def changed(t):
        # print(f"{t} changed {st.session_state[t]}")
        pass

    for defaults in [GenerationInputDefaults, DebuggingParamsDefaults]:
        st.write(f'{defaults.__name__[:-8]}')
        for k, k_type in get_type_hints(defaults).items():
            label = k

            if k not in st.session_state:
                # print(f'init {k}')
                st.session_state[k] = getattr(defaults, k)

            if not AppState.is_general_preset() and k not in AppState.get_chosen_preset_generation_configuration():
                continue

            if k_type == str:
                st.text_input(
                    label=label,
                    key=k,
                    on_change=changed,
                    args=[k]
                )
            elif k_type == int:
                st.number_input(
                    label=label,
                    key=k,
                    min_value=0,
                    on_change=changed,
                    args=[k]
                )
            elif k_type == bool:
                st.checkbox(
                    label=label,
                    key=k,
                    on_change=changed,
                    args=[k]
                )
            elif k_type == float:
                st.number_input(
                    label=label,
                    key=k,
                    min_value=0.0,
                    on_change=changed,
                    args=[k]
                )


def run():
    select_generation_params()

    generation_inputs = AppState.get_generation_inputs()
    with st.expander('Generation Inputs:'):
        st.write(generation_inputs)
