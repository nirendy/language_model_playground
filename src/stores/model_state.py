from typing import List

import streamlit as st
import torch

from src.stores import AppStateKeys
from src.stores import BaseState
from src.stores import ModelID
from src.stores import ModelStateKeys
from src.stores.app_state import AppState
from src.utils.huggingface import encode_input_text
from src.utils.huggingface import generate_model_outputs
from src.utils.huggingface import get_model_and_tokenizer


class ModelState(BaseState[ModelStateKeys]):
    def __init__(self, model_name: ModelID):
        self.model_name = model_name

        self.get_or_create_by_key(ModelStateKeys.model, None)
        self.get_or_create_by_key(ModelStateKeys.tokenizer, None)
        self.get_or_create_by_key(ModelStateKeys.error, None)

    @staticmethod
    def get_active_model_states() -> List["ModelState"]:
        selected_models = AppState().get_by_key(AppStateKeys.selected_models)
        return [ModelState(model_id) for model_id in selected_models]

    def state_prefix(self) -> str:
        return self.model_name

    def prefix_field(self, state_key: ModelStateKeys):
        return super(ModelState, self).prefix_field(state_key)

    def is_loaded(self):
        return self.get_model() is not None

    def get_model(self):
        return st.session_state[self.prefix_field(ModelStateKeys.model)]

    def get_tokenizer(self):
        return st.session_state[self.prefix_field(ModelStateKeys.tokenizer)]

    def load_model(self):
        if self.is_loaded():
            return
        try:
            model, tokenizer = get_model_and_tokenizer(
                task_name=AppState().get_by_key(AppStateKeys.selected_task),
                model_name=self.model_name
            )

            st.session_state[self.prefix_field(ModelStateKeys.model)] = model
            st.session_state[self.prefix_field(ModelStateKeys.tokenizer)] = tokenizer
            st.session_state[self.prefix_field(ModelStateKeys.error)] = None
        except Exception as e:
            print(e)
            st.session_state[self.prefix_field(ModelStateKeys.model)] = None
            st.session_state[self.prefix_field(ModelStateKeys.tokenizer)] = None
            st.session_state[self.prefix_field(ModelStateKeys.error)] = e

    def is_erroneous(self):
        return st.session_state[self.prefix_field(ModelStateKeys.error)] is not None


# def compute_input_ids(model_id: str, input_sentence: str):
#     model_state = ModelState.get_model_state(model_id)
#     return model_state.get_tokenizer().encode(input_sentence, return_tensors='pt')


# @st.cache(allow_output_mutation=True, hash_funcs={tokenizers.Tokenizer: id})
def generate_model_output(model_id: str):
    model_state = ModelState(model_id)
    encoded_input = encode_input_text(
        model_state.get_tokenizer(),
        AppState().get_by_key(AppStateKeys.init_input_tokens)
    )
    torch.manual_seed(AppState().get_by_key(AppStateKeys.seed))

    # initial
    model_outputs = generate_model_outputs(
        model=model_state.get_model(),
        input_ids=encoded_input,
        **AppState().get_generation_inputs()
    )

    return model_outputs
