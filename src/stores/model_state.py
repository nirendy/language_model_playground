import logging
from typing import List

import streamlit as st
from typing import Optional
import torch
from tokenizers import tokenizers

from transformers import PreTrainedModel
from transformers import PreTrainedTokenizer
from transformers import AutoModelForCausalLM, AutoModel
from transformers import AutoTokenizer

from src.stores import AppStateKeys
from src.stores import ModelStateKeys
from src.stores.app_state import AppState
from src.utils.huggingface import encode_input_text
from src.utils.huggingface import generate_model_outputs
from src.utils.huggingface import get_auto_model_by_task
from src.utils.huggingface import get_model_and_tokenizer
from src.utils.streamlit_utils import _init_field


class ModelState:
    def __init__(self, model_name: str):
        self.model_name = model_name

        _init_field(self.prefix_field(ModelStateKeys.model), None)
        _init_field(self.prefix_field(ModelStateKeys.error), None)

    @staticmethod
    def get_active_model_states() -> List["ModelState"]:
        selected_models = AppState.selected_models() or []
        return [ModelState(model_id) for model_id in selected_models]

    def prefix_field(self, model_state_key: ModelStateKeys):
        return f"{self.model_name}_{model_state_key.name}"

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
                task_name=AppState.get_by_key(AppStateKeys.selected_task),
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
    encoded_input = encode_input_text(model_state.get_tokenizer(), AppState.get_init_input_tokens())
    torch.manual_seed(AppState.get_generation_seed())

    # initial
    model_outputs = generate_model_outputs(
        model=model_state.get_model(),
        input_ids=encoded_input,
        **AppState.get_generation_inputs()
    )

    return model_outputs
