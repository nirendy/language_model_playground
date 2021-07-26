import streamlit as st
from typing import Optional

from transformers import PreTrainedModel
from transformers import PreTrainedTokenizer
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer


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
