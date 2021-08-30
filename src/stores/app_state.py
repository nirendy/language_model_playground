from typing import TypeVar

import streamlit as st
from typing import get_type_hints, List
from src.consts import presets as Presets
from src.stores import AppStateKeys
from src.stores import Pages
from src.utils.streamlit_utils import _init_field
from src.utils.streamlit_utils import _is_inited

T = TypeVar('T')

MAX_ALLOWED_MODELS = 2


class GenerationInputDefaults:
    max_length: int = 50
    num_beams: int = 5
    early_stopping: bool = True
    no_repeat_ngram_size: int = 2
    num_return_sequences: int = 5
    do_sample: bool = False
    top_k: int = 0
    temperature: float = 0.7


class DebuggingParamsDefaults:
    seed: int = 0
    number_of_alternative_tokens: int = 4


class AppState:
    @staticmethod
    def init_state():
        _init_field(AppStateKeys.selected_models.name, [])
        # _init_field(AppStateKeys.init_input_tokens.name, Presets.INPUT_TOKENS[0])
        # _init_field(AppStateKeys.selected_page.name, Pages.home)
        AppState.fix_corruption()

    @staticmethod
    def is_inited_by_key(key: AppStateKeys) -> bool:
        return _is_inited(key.name)

    @staticmethod
    def get_or_create_by_key(key: AppStateKeys, default_val: T) -> T:
        return _init_field(key.name, default_val)

    @staticmethod
    def get_by_key(key: AppStateKeys):
        return st.session_state[key.name]

    @staticmethod
    def set_by_key(key: AppStateKeys, new_val):
        st.session_state[key.name] = new_val

    @staticmethod
    def fix_corruption():
        # For some reason values generation values get corrupted
        # Trying to fix the corruption automatically
        warnings = []
        for defaults in [GenerationInputDefaults, DebuggingParamsDefaults]:
            for k, k_type in get_type_hints(defaults).items():
                if k not in st.session_state:
                    continue
                v = st.session_state[k]
                if type(v) != k_type:
                    try:
                        new_val = k_type(v)
                    except Exception as e:
                        st.warning(e)
                        new_val = getattr(defaults, k)

                    warnings.append(f"{k} = {v}, is of type {type(v)} and not of type {k_type}. Changed to {new_val}")
                    st.session_state[k] = new_val

        if len(warnings) > 0:
            # st.warning('Data corruption was detected, automatic fix applied.')
            # with st.expander('Please see the changes below'):
            #     for warning in warnings:
            #         st.write(warning)
            # st.write('___')
            print(warnings)

    @staticmethod
    def clear_cache():
        for key in st.session_state.keys():
            del st.session_state[key]

    @staticmethod
    def get_generation_inputs():
        return {
            k: st.session_state[k]
            for k in get_type_hints(GenerationInputDefaults)
            if (
                    AppState.chosen_generation_preset() == Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]
                    or
                    (k in Presets.TOKEN_GENERATION_CONFIGURATION[AppState.chosen_generation_preset()])
            )
        }

    @staticmethod
    def get_debugging_params():
        return {
            k: st.session_state[k]
            for k in get_type_hints(DebuggingParamsDefaults)
        }

    @staticmethod
    def get_generation_seed() -> int:
        return st.session_state['seed']

    @staticmethod
    def get_init_input_tokens() -> str:
        return st.session_state[AppStateKeys.init_input_tokens.name]

    @staticmethod
    def get_number_of_alternative_tokens() -> int:
        return st.session_state['number_of_alternative_tokens']

    @staticmethod
    def get_num_return_sequences() -> int:
        return st.session_state['num_return_sequences']

    @staticmethod
    def selected_models() -> List[str]:
        return _init_field(AppStateKeys.selected_models.name, [])

    @staticmethod
    def select_model(model_name):
        if len(AppState.selected_models()) <= MAX_ALLOWED_MODELS or model_name not in AppState.selected_models():
            st.session_state[AppStateKeys.selected_models.name].append(model_name)

    @staticmethod
    def deselected_model(model_name):
        if model_name in AppState.selected_models():
            st.session_state[AppStateKeys.selected_models.name].remove(model_name)

    @staticmethod
    def chosen_generation_preset():
        return st.session_state[AppStateKeys.chosen_generation_preset.name]

    @staticmethod
    def get_chosen_preset_generation_configuration():
        if AppState.is_general_preset():
            return None
        return Presets.TOKEN_GENERATION_CONFIGURATION[AppState.chosen_generation_preset()]

    @staticmethod
    def set_chosen_generation_preset():
        if not AppState.is_general_preset():
            for k, v in Presets.TOKEN_GENERATION_CONFIGURATION[AppState.chosen_generation_preset()].items():
                st.session_state[k] = v

    @staticmethod
    def is_general_preset():
        return AppState.chosen_generation_preset() == Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]
