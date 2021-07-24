class Inputs:
    max_length: int = 50
    num_beams: int = 5
    early_stopping: bool = True
    no_repeat_ngram_size: int = 2
    num_return_sequences: int = 5
    do_sample: bool = False
    seed: int = 0
    top_k: int = 0
    temperature: float = 0.7
    number_of_alternative_tokens: int = 4
