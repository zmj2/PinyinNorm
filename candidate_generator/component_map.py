import re

def load_component_dict(dict_path):
    comp_dict = {}
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ' ' not in line:
                continue
            parts, std = line.split(' ')
            comp_dict[parts] = std
    return comp_dict

def lookup_component_map(word, component_dict):
    if word in component_dict:
        return [component_dict[word]]
    return []

def should_use_component_map(word: str) -> bool:
    if not word or len(word) < 2:
        return False
    if not re.fullmatch(r'[\u4e00-\u9fff]+', word):
        return False
    return True