import streamlit as st
from typing import get_type_hints

from src.consts import presets as PRESETS
from src.stores.app_state import DebuggingParamsDefaults
from src.stores.app_state import GenerationInputDefaults, AppState
from src.stores import AppStateKeys
from src.consts.locale import Locale


def render():
    st.selectbox(
        Locale.generation_preset_selectbox_label,
        options=PRESETS.TOKEN_GENERATION_CONFIGURATION_KEYS,
        key=AppStateKeys.chosen_generation_preset.name,
        on_change=AppState().update_generation_params_by_chosen_generation_preset
    )

    # noinspection PyUnusedLocal
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

            if not AppState().is_general_preset and k not in AppState().get_chosen_preset_generation_configuration():
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
