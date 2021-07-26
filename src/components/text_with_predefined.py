import streamlit as st


def select_input_text(key, label, options, on_change=None):
    if on_change is None:
        def nothing():
            pass

        on_change = nothing

    select_box_label = 'Predefined ' + label
    if key not in st.session_state:
        st.session_state[key] = options[0]

    def set_predefined(val):
        st.session_state[key] = val
        on_change()

    text_input_container = st.beta_container()

    with st.beta_expander(select_box_label):
        for i, opt in enumerate(options):
            if i > 0:
                # st.write('___')
                pass

            if st.button(label=opt, key=f'{key}_button_choose_{i}'):
                set_predefined(opt)

            # col1, col2 = st.beta_columns([9, 1])
            # col1.write(opt)
            # if col2.button(label='Choose', key=f'{key}_button_choose_{i}'):
            #     set_predefined(opt)

    with text_input_container:
        st.text_input(
            label=label,
            key=key,
            on_change=on_change
        )


def select_input_text2(key, label, options, on_change=None):
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
