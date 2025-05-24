def generate_by_seq2seq(pinyin_input: str, model=None, tokenizer=None, max_len=10):
    if model is None or tokenizer is None:
        return []