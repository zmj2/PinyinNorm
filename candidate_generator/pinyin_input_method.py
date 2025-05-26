from Pinyin2Hanzi import DefaultDagParams, dag
from itertools import product, chain
from collections import defaultdict

from pypinyin import pinyin, Style
import re


dagparams = DefaultDagParams()

def get_all_valid_pinyin_syllables():
    # 构造一个汉字范围，提取所有拼音
    hanzi_range = [chr(i) for i in range(0x4e00, 0x9fa6)]
    pinyins = set()
    for ch in hanzi_range:
        pys = pinyin(ch, style=Style.NORMAL, strict=False)
        if pys and re.fullmatch(r'[a-z]+', pys[0][0]):
            pinyins.add(pys[0][0])
    return sorted(pinyins)

pinyin_syllables = get_all_valid_pinyin_syllables()

first_letter_index = defaultdict(list)
for py in pinyin_syllables:
    first_letter_index[py[0]].append(py)


def is_first_letter_string(pinyin_str: str, pinyin_syllables: set):
    if ' ' in pinyin_str or len(pinyin_str) < 2 or not pinyin_str.isalpha():
        return False
    
    segments = split_pinyin_string(pinyin_str, pinyin_syllables)
    if all(seg in pinyin_syllables and len(seg) >= 2 for seg in segments) and ''.join(segments) == pinyin_str:
        return False  

    return True  

def expand_first_letter_string(pinyin_str: str, max_expansion=100):
    '''
    如 "nh" -> [["ni", "hao"], ["na", "he"], ...]
    '''
    candidates = []
    letters = list(pinyin_str)
    if any(l not in first_letter_index for l in letters):
        return []

    syllable_options = [first_letter_index[l] for l in letters]
    for seq in product(*syllable_options):
        candidates.append(' '.join(seq))
        if len(candidates) >= max_expansion:
            break
    return candidates

def split_pinyin_string(pinyin_str, pinyin_vocab):
    """
    使用前向最大匹配将拼音串切分为合法音节列表
    """
    i = 0
    result = []
    max_len = max(len(p) for p in pinyin_vocab)
    while i < len(pinyin_str):
        for j in range(max_len, 0, -1):
            candidate = pinyin_str[i:i + j]
            if candidate in pinyin_vocab:
                result.append(candidate)
                i += j
                break
        else:
            # 若找不到，单字符处理
            result.append(pinyin_str[i])
            i += 1
    return result


def generate_from_pinyin2hanzi(pinyin_str: str, topk=5, score_threshold=0.15):
    pinyin_list = pinyin_str.strip().split()
    try:
        results = dag(dagparams, pinyin_list, path_num=topk)
        candidates = []
        for item in results:
            if item.score >= score_threshold:
                try:
                    word = ''.join([node.word for node in item.path])
                except AttributeError:
                    word = ''.join(item.path)
                candidates.append((word, item.score))

        return candidates
    
    except:
        return []
    
def generate_from_pinyin(pinyin_str: str, topk=5, method='pinyin2hanzi', static_dict=None, candidates=None) -> list:
    '''
    输入一个拼音字符串，输出前topk个可能的汉字词。
    '''
    if not pinyin_str.strip():
        return []
    
    if candidates is None:
        candidates = set()
    results = []

    def add(word, score, src):
        if word not in candidates:
            results.append({"word": word, "confidence": score, "source": src})
            candidates.add(word)
    
    if method == 'pinyin2hanzi':
        if is_first_letter_string(pinyin_str, pinyin_syllables):
            expanded_seqs = expand_first_letter_string(pinyin_str)
            for seq in expanded_seqs:
                if static_dict and seq in static_dict:
                    for w in static_dict[seq]:
                        add(w, 0.5, "pinyin_static_dict")
                for w, s in generate_from_pinyin2hanzi(seq, topk):
                    add(w, s - 0.1, "pinyin")
        else:
            if ' ' not in pinyin_str and pinyin_str.isalpha():
                pinyin_str = ' '.join(split_pinyin_string(pinyin_str, pinyin_syllables))
            if static_dict and pinyin_str in static_dict:
                for w in static_dict[pinyin_str]:
                    add(w, 0.5, "pinyin_static_dict")
            for w, s in generate_from_pinyin2hanzi(pinyin_str, topk):
                add(w, s, "pinyin")

        return results
    elif method == 'somiao':
        return []
    else:
        return []
    

def test_pinyin2hanzi(pinyin_str, topk=10):
    print(f"🔍 测试拼音输入：{pinyin_str}")
    pinyin_list = pinyin_str.strip().split()
    results = dag(dagparams, pinyin_list, path_num=topk)

    for i, item in enumerate(results):
        try:
            word = ''.join([node.word for node in item.path])
        except AttributeError:
            word = ''.join(item.path)
        print(f"{i+1:>2}. {word:<10}  得分: {item.score:.4f}")

if __name__ == "__main__":
    test_pinyin2hanzi("jingcha")
