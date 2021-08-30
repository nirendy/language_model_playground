from enum import Enum


class AppStateKeys(Enum):
    selected_models = 0
    init_input_tokens = 1
    chosen_generation_preset = 2
    selected_page = 3
    selected_task = 4


class ModelStateKeys(Enum):
    model = 0
    tokenizer = 1
    error = 2


class Pages(Enum):
    home = "Home"
    task_selection = "Task Selection"
    model_selection = "Model Selection"
    generation_params_tuning = "Generation Params Tuning"
    demo = "Demo"
