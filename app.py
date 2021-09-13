import streamlit as st
from src.consts.locale import Locale
import src.pages.base as base

import gc
import torch

gc.collect()
torch.cuda.empty_cache()

if __name__ == "__main__":
    st.set_page_config(
        page_title=Locale.app_title, page_icon=":memo:",
        layout='wide'
    )

    base.render()
