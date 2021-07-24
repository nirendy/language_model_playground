INPUT_TOKENS = [
    "I enjoy walking with my cute dog",
    'The president of the USA is',
    "Another text",
]

SHARED = {
    'max_length': 50,
    'no_repeat_ngram_size': 2,
}
GREEDY = {
    **SHARED,
}

BEAM_SEARCH = {
    **SHARED,
    'num_return_sequences': 3,
    'num_beams': 5,
    'early_stopping': True
}
RANDOM = {
    **SHARED,
    'num_return_sequences': 3,
    'do_sample': True,
    'seed': 0,
    'top_k': 0,
    'temperature': 0.7,
}

TOKEN_GENERATION_CONFIGURATION = {
    "greedy": GREEDY,
    "beam_search": BEAM_SEARCH,
    'random': RANDOM,
}

TOKEN_GENERATION_CONFIGURATION_KEYS = ['None'] + list(TOKEN_GENERATION_CONFIGURATION.keys())
