from typing import Optional
from typing import Tuple

import streamlit as st
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import PreTrainedModel
from transformers import PreTrainedTokenizer

from src.components.text_with_predefined import select_input_text

available_models = ['None', 'distilgpt2', 'gpt2']


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


@st.cache(allow_output_mutation=True)
def loading_model(model_name: str) -> Model:
    if model_name == 'None':
        return Model('None')

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(model_name, pad_token_id=tokenizer.eos_token_id)

    return Model(model_name, tokenizer, model)


def render():
    if 'is_model_loaded' not in st.session_state:
        st.session_state['model'] = Model()
        st.session_state['is_model_loaded'] = False
        st.session_state['selected_model_name'] = available_models[0]
        st.session_state['is_erroneous_name'] = False

    def model_changed():
        st.session_state['is_erroneous_name'] = False
        st.session_state['is_model_loaded'] = (
                st.session_state['model'].model_name == st.session_state['selected_model_name']
        )

    def load_model():
        try:
            st.session_state['model'] = loading_model(st.session_state['selected_model_name'])
            model_changed()
        except Exception as e:
            print(e)
            st.session_state['is_erroneous_name'] = True

    select_input_text(
        label='Select Model',
        options=available_models,
        key='selected_model_name',
        on_change=model_changed
    )

    if st.session_state['is_erroneous_name']:
        st.write(f"Model named {st.session_state['selected_model_name']} was not found!")

    if not (
            st.session_state['is_erroneous_name']
            or
            st.session_state['is_model_loaded']
            or st.session_state['selected_model_name'] == 'None'
    ):
        st.button(
            label=f"Load {st.session_state['selected_model_name']}",
            on_click=load_model
        )
