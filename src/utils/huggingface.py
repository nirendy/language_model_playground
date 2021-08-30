from transformers import AutoTokenizer
from transformers.pipelines import SUPPORTED_TASKS


def get_auto_model_by_task(task):
    return SUPPORTED_TASKS[task]['pt'][0]


def get_model_and_tokenizer(task_name, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    auto_model = get_auto_model_by_task(task_name)
    model = auto_model.from_pretrained(model_name, pad_token_id=tokenizer.eos_token_id)
    # model = AutoModelForCausalLM.from_pretrained(model_name, pad_token_id=tokenizer.eos_token_id)

    return model, tokenizer


def encode_input_text(tokenizer, input_tokens):
    return tokenizer.encode(input_tokens, return_tensors='pt')


def generate_model_outputs(model, input_ids, **generation_params_kwargs):
    return model.generate(
        input_ids=input_ids,
        **generation_params_kwargs
    )
