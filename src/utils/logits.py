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
        softmax = logit.softmax(0)
        indices = logit.topk(n).indices

        lst = []
        for i in indices:
            lst.append(f"{self.convert_ids_to_token([i])} ({softmax[i]:.2f})")

        return lst

    def get_sequence_logit_top_n_tokens(self, input_ids, sequence_logit, n):
        lst = []
        saw_eof = False
        for i in range(len(input_ids)):
            sub_lst = []
            token_id = input_ids[i].item()
            if token_id == sequence_logit.shape[1] - 1:
                if saw_eof:
                    break
                saw_eof = True
            token_str = self.convert_ids_to_token(token_id)
            if i > 0:
                token_str += f" ({sequence_logit[i - 1].softmax(0)[token_id]:.2f})"
                sub_lst.extend(self.get_logit_top_n_tokens(sequence_logit[i - 1], n))
            lst.append([token_str] + sub_lst)
        return lst
