import streamlit as st

from src.stores import AppStateKeys
from src.stores import Pages
from src.stores.app_state import AppState


def render():
    selected_model = AppState().get_by_key(AppStateKeys.selected_models)
    selected_model_text = ''
    if len(selected_model) > 0:
        selected_model_text = f" ({selected_model[0]} is selected)"

    article_link = "[How to generate text: using different decoding methods for language generation with Transformers](https://huggingface.co/blog/how-to-generate)"
    generate_documentation_link = "[.generate(...)](https://huggingface.co/transformers/main_classes/model.html?highlight=generate#transformers.generation_utils.GenerationMixin.generate)"
    huggingface_models_hub_link = "[Models Hub](https://huggingface.co/models)"
    autoregressive_language_generation_link = "[auto-regressive language generation](http://jalammar.github.io/illustrated-gpt2/)"
    st.write(
        f"""
# Welcome to the Transformers Playground!
### This playground designed as an interactive tutorial for the Transformers library by HuggingFace 🤗
---
## Background
In the article {article_link},
\nPatrick von Platen go through the main decoding methods 
and implements them using the {generate_documentation_link} method provided by Transformers 🤗 library.
\nBased on Patrick's tutorial, this tool will can learn about the different decoding strategies through live examples. 
\nSimilarly to Patrick's tutorial, we will only considered models that supports of {autoregressive_language_generation_link}.

---        
## Let's start!
You are in the Home Page now, you can move steps clicking on the corresponding button.

---
"""
    )
    st.button(
        Pages.model_selection.value,
        on_click=AppState().set_by_key,
        args=(AppStateKeys.selected_page, Pages.model_selection)
    )
    st.write(
        f"""

**Step 1: Choose a model{selected_model_text}**
- Huggingface {huggingface_models_hub_link} provides many models, here you can browse by models that tagged with 'text-generation'
---
"""
    )
    if len(selected_model) > 0:
        st.button(
            Pages.demo.value,
            on_click=AppState().set_by_key,
            args=(AppStateKeys.selected_page, Pages.demo)
        )

    st.write(
        f"""
**Step 2: Choose Input Sentence 🔠**
- Once a model is selected, choose an input sentence to start the demo

**Step 3: Change Generation Params ⚙️**
- You will start with a the greedy strategy, apply changes to the generation params to explore more advanced approach!

**Step 4: Examine Generated Output 🧐**
- Scroll back to see how different decoding strategies impact the generated text

**Step 5: Try Different Input or Different Model 🔃️**
- Use the selectbox on the sidebar to start a new demo, you can always go back to a previous demo.  

---
# YOU ARE READY TO GO!
Start by clicking on the Model Selection Button.
\nYou can return this page for reference at any point!

---
### Settings 
"""
    )

    st.checkbox(
        label='Use GPU (Experimental)',
        key=AppState().prefix_field(AppStateKeys.use_gpu),
        help="GPU can significantly speed up the results.\n"
             "Having said that, it seems that the school provided GPUs aren't stable, "
             "and in that case, using CPU will bring better user experience"
    )
