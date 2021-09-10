class GenerationInput:
    def __init__(
            self,
            name: str,
            input_type,
            description,
            default_val,
            min_val=None,
            max_val=None,
            is_advanced=False,
    ):
        self.name = name
        self.input_type = input_type
        self.description = description
        self.default_val = default_val
        self.min_val = min_val
        self.max_val = max_val
        self.is_advanced = is_advanced

    def get_input_kwargs(self):
        kwargs = {}
        if self.min_val is not None:
            kwargs['min_value'] = self.min_val
        if self.max_val is not None:
            kwargs['max_value'] = self.max_val

        if self.input_type == int:
            kwargs['step'] = 1

        return kwargs


generation_inputs = [
    GenerationInput(
        name='min_length',
        description='The minimum length of the sequence to be generated',
        input_type=int,
        default_val=10,
        min_val=0,
    ),
    GenerationInput(
        name='max_length',
        description='The maximum length of the sequence to be generated.',
        input_type=int,
        default_val=50,
        min_val=0,
    ),
    GenerationInput(
        name='num_beams',
        description='Number of beams for beam search. 1 means no beam search',
        input_type=int,
        default_val=1,
        min_val=1
    ),
    GenerationInput(
        name='early_stopping',
        description='Whether to stop the beam search when at least num_beams sentences are finished per batch or not.',
        input_type=bool,
        default_val=True,
    ),
    GenerationInput(
        name='no_repeat_ngram_size',
        description='If set to int > 0, all ngrams of that size can only occur once.',
        input_type=int,
        min_val=0,
        default_val=0,
    ),
    GenerationInput(
        name='do_sample',
        description='Whether or not to use sampling ; use greedy decoding otherwise.',
        input_type=bool,
        default_val=False,
    ),
    GenerationInput(
        name='top_k',
        description='The number of highest probability vocabulary tokens to keep for top-k-filtering.',
        input_type=int,
        default_val=0,
    ),
    GenerationInput(
        name='top_p',
        description='If set to float < 1, only the most probable tokens with probabilities that add up to top_p or higher are kept for generation.',
        input_type=float,
        default_val=1.0,
    ),
    GenerationInput(
        name='temperature',
        description='The value used to module the next token probabilities.',
        input_type=float,
        default_val=1.0,
    ),
    GenerationInput(
        name='seed',
        description='Seed for random generation',
        input_type=int,
        default_val=0,
    ),
    GenerationInput(
        name='repetition_penalty',
        description='The parameter for repetition penalty. 1.0 means no penalty.',
        input_type=float,
        default_val=1.0,
        is_advanced=True,
    ),
    GenerationInput(
        name='num_beam_groups',
        description='Number of groups to divide num_beams into in order to ensure diversity among different groups of beams. this paper for more details.',
        input_type=int,
        default_val=1,
        is_advanced=True,
    ),
    GenerationInput(
        name='diversity_penalty',
        description='This value is subtracted from a beam’s score if it generates a token same as any beam from other group at a particular time. Note that diversity_penalty is only effective if group beam search is enabled.',
        input_type=float,
        default_val=0.0,
        is_advanced=True,
    ),
]
