from typing import Tuple, get_type_hints

import streamlit as st
import matplotlib as mpl
import tokenizers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, PreTrainedModel
import pandas as pd
import functools
import itertools

from src.utils.logits import TokenizerDebugger


class Texts:
    app_title = 'NLP Playground'
    init_sentence = 'Initial Sentence'
    max_length = 'Max sentence length'
    early_stopping = 'Early stopping'
    no_repeat_ngram_size = 'No repeat n-gram size'
    num_return_sequences = 'Num return sequences'


class Inputs:
    init_sentence: str = "I enjoy walking with my cute dog"
    max_length: int = 50
    num_beams: int = 5
    early_stopping: bool = True
    no_repeat_ngram_size: int = 2
    num_return_sequences: int = 5
    do_sample: bool = False
    seed: int = 0
    top_k: int = 0
    temperature: float = 0.7

    number_of_alternative_tokens: int = 4


st.set_page_config(page_title=Texts.app_title, page_icon=":memo:")


@st.cache(allow_output_mutation=True)
def loading_model() -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

    model = AutoModelForCausalLM.from_pretrained("distilgpt2", pad_token_id=tokenizer.eos_token_id)
    return tokenizer, model


@st.cache(hash_funcs={tokenizers.Tokenizer: id})
def compute_input_ids(tokenizer, input_sentence):
    return tokenizer.encode(input_sentence, return_tensors='pt')


def run():
    tokenizer, model = loading_model()

    for k, k_type in get_type_hints(Inputs).items():
        if k_type == str:
            setattr(Inputs, k, st.sidebar.text_input(
                k,
                Inputs.init_sentence,
            ))
        elif k_type == int:
            setattr(Inputs, k, st.sidebar.number_input(
                label=k,
                value=getattr(Inputs, k),
                min_value=0
            ))
        elif k_type == bool:
            setattr(Inputs, k, st.sidebar.checkbox(
                k,
                getattr(Inputs, k),
            ))
        elif k_type == float:
            setattr(Inputs, k, st.sidebar.number_input(
                label=k,
                value=getattr(Inputs, k),
                min_value=0.0
            ))

    input_ids = compute_input_ids(tokenizer, Inputs.init_sentence)
    torch.manual_seed(Inputs.seed)

    # initial
    model_outputs = model.generate(
        input_ids=input_ids,
        max_length=Inputs.max_length,
        num_beams=Inputs.num_beams,
        early_stopping=Inputs.early_stopping,
        no_repeat_ngram_size=Inputs.no_repeat_ngram_size,
        num_return_sequences=Inputs.num_return_sequences,
        do_sample=Inputs.do_sample,
        temperature=Inputs.temperature,
    )

    "Output:"

    tokenizer_debugger = TokenizerDebugger(tokenizer)

    for i, model_output in enumerate(model_outputs):
        st.write("\n " + 100 * '-')
        st.write(tokenizer.decode(model_output, skip_special_tokens=True))

        generated_model = model(model_output)
        res = tokenizer_debugger.get_sequence_logit_top_n_tokens(model_output, generated_model.logits,
                                                                 Inputs.number_of_alternative_tokens)
        st.dataframe(pd.DataFrame(res).fillna(''))


if __name__ == "__main__":
    run()
