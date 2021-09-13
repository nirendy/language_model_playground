import streamlit as st

from src.components.text_with_predefined import select_input_text
from src.consts.generation_input_options import GenerationInput
from src.consts.generation_input_options import generation_inputs
from src.stores import DemoID
from src.stores import DemoStateKeys
from src.stores import DemoStepStateKeys
from src.stores.app_state import AppState
from src.stores.demo_state import DemoState
from src.stores.demo_step_state import DemoStepState
from src.stores import AppStateKeys
from src.consts.locale import Locale
import src.consts.presets as PRESETS


def render_input_param(generation_input: GenerationInput):
    if generation_input.input_type == str:
        return st.text_input
    elif generation_input.input_type == int:
        return st.number_input
    elif generation_input.input_type == bool:
        return st.checkbox
    elif generation_input.input_type == float:
        return st.number_input


def demo_selection():
    demo_counter = AppState().get_or_create_by_key(AppStateKeys.demo_counter, 1)
    selected_demo: DemoID = AppState().get_or_create_by_key(AppStateKeys.selected_demo, 1)
    demo_state = DemoState(selected_demo)

    with st.sidebar:
        st.write('___')
        st.selectbox(
            label='Demo History',
            key=AppState().prefix_field(AppStateKeys.selected_demo),
            options=list(range(1, demo_counter + 1)),
            format_func=lambda n: "Create New Demo" if n == demo_counter else f"Demo #{n}"
        )
        st.write('Model Selected:')
        if demo_state.is_started:
            st.write(demo_state.get_by_key(DemoStateKeys.model_id))
        elif AppState().is_model_selected:
            st.write(AppState().get_by_key(AppStateKeys.selected_models)[0])


def start_demo():
    demo_counter = AppState().get_or_create_by_key(AppStateKeys.demo_counter, 1)
    selected_demo: DemoID = AppState().get_or_create_by_key(AppStateKeys.selected_demo, 1)
    demo_state = DemoState(selected_demo)
    input_text = AppState().get_by_key(AppStateKeys.init_input_tokens)

    demo_state.start(
        model_id=AppState().get_by_key(AppStateKeys.selected_models)[0],
        input_text=input_text
    )
    AppState().set_by_key(AppStateKeys.demo_counter, demo_counter + 1)
    DemoStepState.start_first(selected_demo)

    # print('1')
    # st.experimental_rerun()


def non_started_content():
    with st.container():
        select_input_text(
            key=AppState().prefix_field(AppStateKeys.init_input_tokens),
            label=Locale.init_sentence,
            options=PRESETS.INPUT_TOKENS,
            use_text_area=True
        )

    with st.sidebar:
        st.write('___')
        input_text = AppState().get_by_key(AppStateKeys.init_input_tokens)
        if AppState().is_model_selected and input_text:
            st.button('Start Demo', on_click=start_demo)


def steps():
    selected_demo: DemoID = AppState().get_or_create_by_key(AppStateKeys.selected_demo, 1)
    demo_state = DemoState(selected_demo)

    for i in range(1, demo_state.get_by_key(DemoStateKeys.steps_counter) + 1):
        demo_step_state = DemoStepState(selected_demo, i)
        expander = st.expander(f'Step {i}: {demo_step_state.get_description()}', expanded=False)

        if demo_step_state.is_started:
            st.write(demo_step_state.decoded_output())
            expander.write(demo_step_state.get_by_key(DemoStepStateKeys.generation_params))
            expander.write(demo_step_state.logits_table())

        st.write('___')


def render():
    selected_demo: DemoID = AppState().get_or_create_by_key(AppStateKeys.selected_demo, 1)
    demo_state = DemoState(selected_demo)

    demo_selection()

    if not demo_state.is_started:
        non_started_content()
    else:
        st.write("Input Sentence:")
        st.write(demo_state.get_by_key(DemoStateKeys.input_text))
        st.write('___')

        with st.sidebar:
            st.write('___')
            cur_generations_params = (
                DemoStepState(selected_demo, demo_state.get_by_key(DemoStateKeys.steps_counter))
                    .get_by_key(DemoStepStateKeys.generation_params)
            )
            next_demo_step_state = DemoStepState(selected_demo, demo_state.get_by_key(DemoStateKeys.steps_counter) + 1)
            st.write(cur_generations_params)

        steps()

        with st.expander(
                'Modify Generation Input',
                expanded=True
        ):
            for generation_input in generation_inputs:
                should_show_input = (
                        next_demo_step_state.is_inited_by_key(DemoStepStateKeys.generation_input_changed)
                        and
                        next_demo_step_state.get_by_key(DemoStepStateKeys.generation_input_changed) == generation_input
                )

                if should_show_input:
                    st.write('---')

                cols = st.columns([0.2, 0.2, 0.6])
                cols[0].write(generation_input.name)

                if should_show_input:
                    generation_input = next_demo_step_state.get_by_key(DemoStepStateKeys.generation_input_changed)
                    old_val = (
                        cur_generations_params[generation_input.name]
                        if generation_input.name in cur_generations_params
                        else None
                    )
                    next_demo_step_state.get_or_create_by_key(
                        DemoStepStateKeys.generation_input_new_value,
                        (old_val if (old_val is not None) else generation_input.default_val)
                    )
                    input_component = render_input_param(generation_input)

                    with cols[1]:
                        new_val = input_component(
                            label=f"Set {generation_input.name}",
                            key=next_demo_step_state.prefix_field(DemoStepStateKeys.generation_input_new_value),
                            help=generation_input.description,
                            **generation_input.get_input_kwargs()
                        )

                    if not ((new_val == old_val) or (new_val is old_val)):
                        cols[1].button('Launch Next Step', on_click=next_demo_step_state.start)
                    st.write('---')

                elif cols[1].button(f'Set', key=f'set_{generation_input.name}'):
                    next_demo_step_state.delete_by_key(DemoStepStateKeys.generation_input_new_value)
                    next_demo_step_state.set_by_key(DemoStepStateKeys.generation_input_changed, generation_input)

                    print('2')
                    st.experimental_rerun()

                cols[2].write(generation_input.description)
