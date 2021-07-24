import streamlit as st
import pandas as pd

from src.components.model_selector import Model


def run(model: Model, model_outputs, tokenizer_debugger):
    for i, model_output in enumerate(model_outputs):
        st.write("\n " + 100 * '-')
        st.write(model.tokenizer.decode(model_output, skip_special_tokens=True))

        generated_model = model.model(model_output)
        res = tokenizer_debugger.get_sequence_logit_top_n_tokens(model_output, generated_model.logits,
                                                                 st.session_state['number_of_alternative_tokens'])
        st.dataframe(pd.DataFrame(res).fillna(''))
