import streamlit as st
import pandas as pd

from src.consts.app_state import ModelState, AppState


def render(model_state: ModelState, model_outputs, tokenizer_debugger):
    for i, model_output in enumerate(model_outputs):
        if i > 0:
            st.write('___')

        st.text(model_state.get_tokenizer().decode(model_output, skip_special_tokens=True))

        generated_model = model_state.get_model()(model_output)
        res = tokenizer_debugger.get_sequence_logit_top_n_tokens(
            model_output, generated_model.logits,
            AppState.get_number_of_alternative_tokens()
        )

        st.dataframe(pd.DataFrame(res).fillna(''))
