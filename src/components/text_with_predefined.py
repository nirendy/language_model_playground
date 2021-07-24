import streamlit as st


def select_input_text(key, label, options, on_change=None):
    if on_change is None:
        def nothing():
            pass

        on_change = nothing

    select_box_key = 'predefined_' + key
    select_box_label = 'Predefined ' + label
    if key not in st.session_state:
        st.session_state[key] = options[0]
        st.session_state[select_box_key] = options[0]

    def set_predefined():
        st.session_state[key] = st.session_state[select_box_key]
        on_change()

    st.selectbox(
        label=select_box_label,
        options=options,
        key=select_box_key,
        on_change=set_predefined
    )

    st.text_input(
        label=label,
        key=key,
        on_change=on_change
    )
