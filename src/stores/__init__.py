import abc
from enum import Enum

import streamlit as st


class AppStateKeys(Enum):
    selected_models = 0
    init_input_tokens = 1
    chosen_generation_preset = 2
    selected_page = 3
    selected_task = 4
    number_of_alternative_tokens = 5
    num_return_sequences = 6
    seed = 7


class ModelStateKeys(Enum):
    model = 0
    tokenizer = 1
    error = 2


from typing import Generic, TypeVar

StateKeyT = TypeVar("StateKeyT", Enum, Enum)
T = TypeVar('T')


class BaseState(abc.ABC, Generic[StateKeyT]):
    @abc.abstractmethod
    def state_prefix(self) -> str:
        pass

    def prefix_field(self, state_key: StateKeyT) -> str:
        return f"{self.state_prefix()}{state_key.name}"

    def is_inited_by_key(self, key: StateKeyT) -> bool:
        return self.prefix_field(key) in st.session_state

    def get_or_create_by_key(self, key: StateKeyT, default_val: T) -> T:
        if not self.is_inited_by_key(key):
            self.set_by_key(key, default_val)

        return self.get_by_key(key)

    def get_by_key(self, key: StateKeyT):
        return st.session_state[self.prefix_field(key)]

    def set_by_key(self, key: StateKeyT, new_val):
        st.session_state[self.prefix_field(key)] = new_val

    @staticmethod
    def clear_all_caches():
        for key in st.session_state.keys():
            del st.session_state[key]


class Pages(Enum):
    home = "Home"
    task_selection = "Task Selection"
    model_selection = "Model Selection"
    generation_params_tuning = "Generation Params Tuning"
    demo = "Demo"
