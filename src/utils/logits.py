from transformers import PreTrainedTokenizer

class TokenizerDebugger:
    def __init__(self, tokenizer: PreTrainedTokenizer):
        self.tokenizer: PreTrainedTokenizer = tokenizer

    def convert_ids_to_token(self, ids):
        return self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(
                ids, skip_special_tokens=True
            )
        ).strip()

    def get_logit_top_n_tokens(self, logit, n):
        return self.convert_ids_to_token(
            logit.topk(n).indices
        ).strip().split(' ')

    def get_sequence_logit_top_n_tokens(self, input_ids, sequence_logit, n):
        lst = []
        for i in range(len(input_ids)):
            sub_lst = []
            token_str = self.convert_ids_to_token(input_ids[i].item())
            sub_lst.append(token_str)
            if i > 0:
                sub_lst.extend(self.get_logit_top_n_tokens(sequence_logit[i - 1], n))
            lst.append(sub_lst)
        return lst
