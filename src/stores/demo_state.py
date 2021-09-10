from src.stores import BaseState
from src.stores import DemoID
from src.stores import DemoStateKeys
from src.stores import ModelID
from src.stores.model_state import ModelState


class DemoState(BaseState[DemoStateKeys]):
    def __init__(self, demo_number: DemoID):
        self.demo_number = demo_number

    def state_prefix(self) -> str:
        return f"demo{self.demo_number}"

    @property
    def is_started(self) -> bool:
        return self.is_inited_by_key(DemoStateKeys.steps_counter)

    def increment_step_counter(self) -> bool:
        prev_counter = self.get_by_key(DemoStateKeys.steps_counter)
        return self.set_by_key(DemoStateKeys.steps_counter, prev_counter + 1)

    @property
    def model_state(self) -> ModelState:
        return ModelState(self.get_by_key(DemoStateKeys.model_id))

    def start(self, model_id: ModelID, input_text: str):
        if self.is_started:
            raise Exception('Unexpected Code')
        self.set_by_key(DemoStateKeys.input_text, input_text)
        self.set_by_key(DemoStateKeys.model_id, model_id)
        self.set_by_key(DemoStateKeys.steps_counter, 1)
