import pandas as pd
import torch
import streamlit as st

from src.consts.generation_input_options import GenerationInput
from src.consts.generation_input_options import generation_inputs
from src.stores import AppStateKeys
from src.stores import BaseState
from src.stores import DemoID
from src.stores import DemoStateKeys
from src.stores import DemoStepID
from src.stores import DemoStepStateKeys
from src.stores import ModelID
import src.consts.presets as PRESETS
from src.stores.app_state import AppState
from src.stores.demo_state import DemoState
from src.utils.huggingface import encode_input_text
from src.utils.huggingface import generate_model_outputs
from src.utils.logits import TokenizerDebugger


class DemoStepState(BaseState[DemoStepStateKeys]):
    def __init__(self, demo_number: DemoID, demo_step: DemoStepID):
        self.demo_number = demo_number
        self.demo_step = demo_step

    def state_prefix(self) -> str:
        return f"demo{self.demo_number}step{self.demo_step}"

    @property
    def is_first(self) -> bool:
        return not self.is_inited_by_key(DemoStepStateKeys.generation_input_changed)

    @property
    def is_started(self) -> bool:
        return self.is_inited_by_key(DemoStepStateKeys.model_output)

    @property
    def demo_state(self) -> DemoState:
        return DemoState(self.demo_number)

    @property
    def prev_demo_step_state(self) -> "DemoStepState":
        return DemoStepState(self.demo_number, self.demo_step - 1)

    @classmethod
    def start_first(cls, model_id: ModelID):
        demo_step = cls(model_id, 1)
        model_state = demo_step.demo_state.model_state
        model_state.load_model()
        model = model_state.get_model()

        demo_step.set_by_key(
            DemoStepStateKeys.generation_params,
            {
                generation_input.name: (
                    generation_input.default_val
                    if generation_input.default_val is not None
                    else getattr(model.config, generation_input.name)
                )
                for generation_input in generation_inputs
            }
        )

        demo_step.start()

    def start(self):
        if self.is_started:
            raise Exception('Unexpected Code')

        if not self.is_first:
            prev_generation_params: dict = self.prev_demo_step_state.get_by_key(DemoStepStateKeys.generation_params)
            new_generation_params = prev_generation_params.copy()
            generation_input: GenerationInput = self.get_by_key(DemoStepStateKeys.generation_input_changed)
            new_value = self.get_by_key(DemoStepStateKeys.generation_input_new_value)
            if new_value is None:
                del new_generation_params[generation_input.name]
            else:
                new_generation_params[generation_input.name] = new_value

            self.set_by_key(DemoStepStateKeys.generation_params, new_generation_params)
            self.demo_state.increment_step_counter()

        model_state = self.demo_state.model_state
        model_state.load_model()
        generation_params = self.get_by_key(DemoStepStateKeys.generation_params)
        encoded_input = encode_input_text(
            model_state.get_tokenizer(),
            self.demo_state.get_by_key(DemoStateKeys.input_text)
        )

        if AppState().get_by_key(AppStateKeys.use_gpu):
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            try:
                encoded_input = encoded_input.to(device)
            except Exception as err:
                print(err)
                st.warning(f"Could not load text to GPU\n{err}")

        if 'seed' in generation_params:
            torch.manual_seed(generation_params['seed'])

        model_outputs = generate_model_outputs(
            model=model_state.get_model(),
            input_ids=encoded_input,
            **{
                k: v
                for k, v in generation_params.items()
                if not ((k in ['seed']) or (v is None))
            }
        )

        self.set_by_key(DemoStepStateKeys.model_output, model_outputs)

    def decoded_output(self):
        model_state = self.demo_state.model_state
        model_output = self.get_by_key(DemoStepStateKeys.model_output)[0]
        return model_state.get_tokenizer().decode(model_output, skip_special_tokens=True)

    def logits_table(self):
        model_state = self.demo_state.model_state
        model_output = self.get_by_key(DemoStepStateKeys.model_output)[0]

        tokenizer_debugger = TokenizerDebugger(model_state.get_tokenizer())
        generated_model = model_state.get_model()(model_output)
        res = tokenizer_debugger.get_sequence_logit_top_n_tokens(
            input_ids=model_output,
            sequence_logit=generated_model.logits,
            n=5  # AppState().get_by_key(AppStateKeys.number_of_alternative_tokens)
        )

        return pd.DataFrame(res).fillna('')

    def get_description(self) -> str:
        if self.is_first:
            return 'Greed Search'
        generation_input: GenerationInput = self.get_by_key(DemoStepStateKeys.generation_input_changed)
        new_value = self.get_by_key(DemoStepStateKeys.generation_input_new_value)
        if new_value is None:
            return f"'{generation_input.name}' is removed"

        return f"'{generation_input.name}' changed to '{new_value}'"
