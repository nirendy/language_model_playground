from typing import List

import streamlit as st
from typing import Optional
import torch
from tokenizers import tokenizers

from transformers import PreTrainedModel
from transformers import PreTrainedTokenizer
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from src.stores.app_state import AppState
from src.utils.streamlit_utils import _init_field

available_models = ['None', 'distilgpt2', 'gpt2']


class ModelState:
    def __init__(self, model_name: str):
        self.model_name = model_name

        _init_field(self.prefix_field('model'), Model())
        _init_field(self.prefix_field('is_model_loaded'), False)
        _init_field(self.prefix_field('is_erroneous_name'), False)

    @staticmethod
    def get_model_state(model_id: str) -> "ModelState":
        return ModelState(model_id)

    @staticmethod
    def get_active_model_states() -> List["ModelState"]:
        selected_models = AppState.selected_models() or []

        return [ModelState.get_model_state(model_id) for model_id in selected_models]

    def prefix_field(self, field):
        return f"{self.model_name}_{field}"

    def is_loaded(self):
        return st.session_state[self.prefix_field('is_model_loaded')]

    def get_model(self):
        return st.session_state[self.prefix_field('model')].model

    def get_tokenizer(self):
        return st.session_state[self.prefix_field('model')].tokenizer

    def model_changed(self):
        st.session_state[self.prefix_field('is_erroneous_name')] = False
        st.session_state[self.prefix_field('is_model_loaded')] = (
                st.session_state[self.prefix_field('model')].model_name == self.model_name)

    def load_model(self):
        try:
            st.session_state[self.prefix_field('model')] = loading_model(self.model_name)
            self.model_changed()
        except Exception as e:
            print(e)
            st.session_state[self.prefix_field('is_erroneous_name')] = True

    def is_erroneous_name(self):
        return st.session_state[self.prefix_field('is_erroneous_name')]

    def should_show_load_button(self):
        return not (
                st.session_state[self.prefix_field('is_erroneous_name')]
                or
                st.session_state[self.prefix_field('is_model_loaded')]
        )


class Model:
    def __init__(self,
                 model_name: Optional[str] = None,
                 tokenizer: Optional[PreTrainedTokenizer] = None,
                 model: Optional[PreTrainedModel] = None
                 ):
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.model = model

    def is_model_loaded(self):
        return self.model is not None


# @st.cache(allow_output_mutation=True, )
def loading_model(model_name: str) -> Model:
    if model_name == 'None':
        return Model('None')

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(model_name, pad_token_id=tokenizer.eos_token_id)

    return Model(model_name, tokenizer, model)


# def compute_input_ids(model_id: str, input_sentence: str):
#     model_state = ModelState.get_model_state(model_id)
#     return model_state.get_tokenizer().encode(input_sentence, return_tensors='pt')

@st.cache(allow_output_mutation=True, hash_funcs={tokenizers.Tokenizer: id})
def compute_input_ids(tokenizer, input_tokens):
    return tokenizer.encode(input_tokens, return_tensors='pt')


# @st.cache(allow_output_mutation=True, hash_funcs={tokenizers.Tokenizer: id})
def generate_model_output(model_id: str):
    model_state = ModelState.get_model_state(model_id)
    input_ids = compute_input_ids(model_state.get_tokenizer(), AppState.get_init_input_tokens())
    torch.manual_seed(AppState.get_generation_seed())

    # initial
    model_outputs = model_state.get_model().generate(
        input_ids=input_ids,
        **AppState.get_generation_inputs()
    )

    return model_outputs
