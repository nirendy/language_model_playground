import streamlit as st
from typing import get_type_hints, List
from src.consts import presets as Presets
from src.stores import ModelStateKeys
from src.utils.streamlit_utils import _init_field


class GenerationInputDefaults:
    max_length: int = 50
    num_beams: int = 5
    early_stopping: bool = True
    no_repeat_ngram_size: int = 2
    num_return_sequences: int = 5
    do_sample: bool = False
    seed: int = 0
    top_k: int = 0
    temperature: float = 0.7


class DebuggingParamsDefaults:
    number_of_alternative_tokens: int = 4


class AppState:
    @staticmethod
    def init_state():
        _init_field(ModelStateKeys.init_input_tokens.name, Presets.INPUT_TOKENS[0])

        AppState.fix_corruption()

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
    def get_generation_seed() -> int:
        return st.session_state['seed']

    @staticmethod
    def get_init_input_tokens() -> str:
        return st.session_state[ModelStateKeys.init_input_tokens.name]

    @staticmethod
    def get_number_of_alternative_tokens() -> int:
        return st.session_state['number_of_alternative_tokens']

    @staticmethod
    def get_num_return_sequences() -> int:
        return st.session_state['num_return_sequences']

    @staticmethod
    def selected_models() -> List[str]:
        return _init_field(ModelStateKeys.selected_models.name, [])

    @staticmethod
    def chosen_generation_preset():
        return st.session_state[ModelStateKeys.chosen_generation_preset.name]

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
