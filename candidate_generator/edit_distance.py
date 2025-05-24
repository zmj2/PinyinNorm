import Levenshtein
import re

def generate_by_edit_distance(word, vocab, threshold=0.75):
    '''
    字形相似匹配，用于处理错别字。
    返回在给定词表vocab中与word编辑距离不超过max_dist的词。
    '''
    candidates = []
    for cand in vocab:
        if Levenshtein.ratio(word, cand) >= threshold:
            candidates.append(cand)
    return candidates


def should_use_edit_distance(word: str):
    """
    判断是否是全中文；若是混合拼音+汉字，则看是否主要是中文。
    """
    if re.fullmatch(r'[\u4e00-\u9fff]+', word):
        return True
    elif re.fullmatch(r'[a-zA-Z]+', word):
        return False
    elif re.search(r'[a-zA-Z]', word) and re.search(r'[\u4e00-\u9fff]', word):
        num_cn = len(re.findall(r'[\u4e00-\u9fff]', word))
        return num_cn >= 2
    else:
        return False
