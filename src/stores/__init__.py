import abc
import enum
from typing import TypeVar

import streamlit as st

ModelID = TypeVar('ModelID', str, str)
DemoID = TypeVar('DemoID', int, int)
DemoStepID = TypeVar('DemoStepID', int, int)


class AppStateKeys(enum.Enum):
    selected_models = enum.auto()
    init_input_tokens = enum.auto()
    chosen_generation_preset = enum.auto()
    selected_page = enum.auto()
    selected_task = enum.auto()
    number_of_alternative_tokens = enum.auto()
    num_return_sequences = enum.auto()
    seed = enum.auto()
    demo_counter = enum.auto()
    selected_demo = enum.auto()


class ModelStateKeys(enum.Enum):
    model = enum.auto()
    tokenizer = enum.auto()
    error = enum.auto()


class DemoStateKeys(enum.Enum):
    input_text = enum.auto()
    model_id = enum.auto()
    steps_counter = enum.auto()


class DemoStepStateKeys(enum.Enum):
    generation_params = enum.auto()
    generation_input_changed = enum.auto()
    generation_input_new_value = enum.auto()
    model_output = enum.auto()


from typing import Generic, TypeVar

StateKeyT = TypeVar("StateKeyT", enum.Enum, enum.Enum)
T = TypeVar('T')


class BaseState(abc.ABC, Generic[StateKeyT]):
    @abc.abstractmethod
    def state_prefix(self) -> str:
        pass

    def prefix_field(self, state_key: StateKeyT) -> str:
        return f"{self.state_prefix()}_{state_key.name}"

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

    def delete_by_key(self, key: StateKeyT):
        if self.prefix_field(key) in st.session_state:
            del st.session_state[self.prefix_field(key)]

    @staticmethod
    def clear_all_caches():
        for key in st.session_state.keys():
            del st.session_state[key]


class Pages(enum.Enum):
    home = "Home"
    task_selection = "Task Selection"
    model_selection = "Model Selection"
    generation_params_tuning = "Generation Params Tuning"
    demo = "Demo"
