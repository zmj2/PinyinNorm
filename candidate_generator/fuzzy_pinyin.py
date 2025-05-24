from candidate_generator.pinyin_input_method import generate_from_pinyin, split_pinyin_string, pinyin_syllables
from itertools import product

pinyin_similarity_map = {
    "zh": ["z", "j"], "z": ["zh"],
    "ch": ["c", "q"], "c": ["ch"],
    "sh": ["s", "x"], "s": ["sh"],
    "l": ["n"], "n": ["l"],
    "f": ["h"], "h": ["f"],

}

def expand_fuzzy(py):
    expanded = [py]
    for key, val_list in pinyin_similarity_map.items():
        if key in py:
            for alt in val_list:
                expanded.append(py.replace(key, alt))
    return list(set(expanded))

def generate_by_fuzzy_pinyin(origin_pinyin, pinyin_to_words, topk=5):

    if isinstance(origin_pinyin, str):
        if ' ' not in origin_pinyin:
            origin_pinyin = split_pinyin_string(origin_pinyin, pinyin_syllables)
        else:
            origin_pinyin = origin_pinyin.strip().split()

    fuzzy_lists = [expand_fuzzy(p) for p in origin_pinyin]

    fuzzy_pinyin_seqs = [' '.join(seq) for seq in product(*fuzzy_lists)]
    
    candidates = set()
    results = []

    for idx, py_seq in enumerate(fuzzy_pinyin_seqs):
        if py_seq in pinyin_to_words:
            for w in pinyin_to_words[py_seq]:
                if w not in candidates:
                    results.append({"word": w, "source": "static_dict", "confidence": 0.6 - idx * 0.01})

        new = generate_from_pinyin(py_seq, topk=topk, static_dict=pinyin_to_words)
        for item in new:
            if item["word"] not in candidates:
                item["source"] = "fuzzy_pinyin"
                item["confidence"] = min(item.get("confidence", 0.5), 0.5 - idx * 0.01)
                results.append(item)
                candidates.add(item["word"])
    
    return results