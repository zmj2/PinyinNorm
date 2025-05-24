from pypinyin import lazy_pinyin
import re

def normalize_to_pinyin(word):

    if not re.search(r'[\u4e00-\u9fff]', word):
        return word.strip(), word.strip()
    
    full_pinyin_seq = []
    first_letter_seq = []
    buffer = ""

    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            if buffer:
                full_pinyin_seq.append(buffer)
                first_letter_seq.append(buffer[0])
                buffer = ""
            py = lazy_pinyin(ch)[0]
            full_pinyin_seq.append(py)
            first_letter_seq.append(py[0])
        elif ch.isalpha():
            buffer += ch
        else:
            if buffer:
                full_pinyin_seq.append(buffer)
                first_letter_seq.append(buffer[0])
                buffer = ""
    if buffer:
        full_pinyin_seq.append(buffer)
        first_letter_seq.append(buffer[0])

    return ' '.join(full_pinyin_seq), ''.join(first_letter_seq)
