from typing import get_type_hints

import streamlit as st

# noinspection PyPep8Naming
from src.consts import presets as Presets
from src.stores import AppStateKeys
from src.stores import BaseState
from src.stores import Pages

MAX_ALLOWED_MODELS = 1


class GenerationInputDefaults:
    min_length: int = 0
    max_length: int = 50
    num_beams: int = 5
    early_stopping: bool = True
    no_repeat_ngram_size: int = 2
    do_sample: bool = False
    top_k: int = 0
    temperature: float = 0.7
    seed: int = 0
    repetition_penalty: float = 1


class DebuggingParamsDefaults:
    num_return_sequences: int = 5
    number_of_alternative_tokens: int = 4


class AppState(BaseState[AppStateKeys]):
    def state_prefix(self) -> str:
        return "app"

    @classmethod
    def init_state(cls):
        cls().get_or_create_by_key(AppStateKeys.selected_models, [])
        cls().get_or_create_by_key(AppStateKeys.use_gpu, False)
        cls().get_or_create_by_key(AppStateKeys.selected_task, 'text-generation')
        cls().fix_corruption()

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

    def get_generation_inputs(self):
        return {
            k: st.session_state[k]
            for k in get_type_hints(GenerationInputDefaults)
            if self.is_general_preset or (k in self.get_chosen_preset_generation_configuration())
        }

    @staticmethod
    def get_debugging_params():
        return {
            k: st.session_state[k]
            for k in get_type_hints(DebuggingParamsDefaults)
        }

    def select_model(self, model_name: str):
        selected_models = self.get_by_key(AppStateKeys.selected_models)
        if (len(selected_models) <= MAX_ALLOWED_MODELS) or (model_name not in selected_models):
            selected_models.append(model_name)

        if len(selected_models) == MAX_ALLOWED_MODELS:
            self.set_by_key(AppStateKeys.selected_page, Pages.demo)

    def deselected_model(self, model_name: str):
        selected_models = self.get_by_key(AppStateKeys.selected_models)
        if model_name in selected_models:
            selected_models.remove(model_name)

    def get_chosen_preset_generation_configuration(self):
        if self.is_general_preset:
            return {}
        return Presets.TOKEN_GENERATION_CONFIGURATION[self.get_by_key(AppStateKeys.chosen_generation_preset)]

    def update_generation_params_by_chosen_generation_preset(self):
        for k, v in self.get_chosen_preset_generation_configuration().items():
            st.session_state[k] = v

    @property
    def is_general_preset(self):
        return self.get_by_key(AppStateKeys.chosen_generation_preset) == Presets.TOKEN_GENERATION_CONFIGURATION_KEYS[0]

    @property
    def is_model_selected(self):
        return len(AppState().get_by_key(AppStateKeys.selected_models)) > 0
