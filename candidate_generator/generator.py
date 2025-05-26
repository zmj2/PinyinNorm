from candidate_generator.static_dict import load_static_dict
from candidate_generator.edit_distance import generate_by_edit_distance, should_use_edit_distance
from candidate_generator.fuzzy_pinyin import generate_by_fuzzy_pinyin
from candidate_generator.pinyin_input_method import generate_from_pinyin
from candidate_generator.component_map import load_component_dict, lookup_component_map, should_use_component_map
from candidate_generator.seq2seq_model import *
from candidate_generator.unified_pinyin import normalize_to_pinyin
from pypinyin import lazy_pinyin
from collections import defaultdict
import re

class CandidateGenerator:
    def __init__(self, dict_path="candidate_generator/dict/规范词典2000条_clean.txt", component_path="candidate_generator/dict/component_map.txt"):
        self.norm_dict = load_static_dict(dict_path)
        self.component_dict = load_component_dict(component_path)
        self.norm_vocab = set(self.norm_dict.values()) | set(self.norm_dict.keys())
        self.pinyin_to_words = self.build_pinyin_index(self.norm_vocab)
        self.static_pinyin_dict = self.build_pinyin_key_dict(self.norm_dict)
    
    def build_pinyin_index(self, word_list):
        index = defaultdict(set)
        for word in word_list:
            pinyin = ' '.join(lazy_pinyin(word))
            index[pinyin].add(word)
        return index
    
    def build_pinyin_key_dict(self, norm_dict):
        from pypinyin import lazy_pinyin
        pinyin_map = {}
        for k, v in norm_dict.items():
            py_key = ' '.join(lazy_pinyin(k))
            pinyin_map[py_key] = v
        return pinyin_map
    
    def get_candidates(self, word):
        candidates = []
        added = set()

        # 1 原词保留
        candidates.append({"word": word, "source": "original"})
        added.add(word)

        # 2 静态词典替换
        if word in self.norm_dict:
            w = self.norm_dict[word]
            if w not in added:
                candidates.append({"word": w, "source": "static_dict"})
                added.add(w)

        # 3 部件组合
        if should_use_component_map(word):
            comp_words = lookup_component_map(word, self.component_dict)
            for w in comp_words:
                if w not in added:
                    candidates.append({"word": w, "source": "component"})
                    added.add(w)

        # 4 拼音精确匹配
        py = ' '.join(lazy_pinyin(word))
        if py in self.static_pinyin_dict:
            w = self.static_pinyin_dict[py]
            if w not in added:
                candidates.append({"word": w, "source": "pinyin_static"})
                added.add(w)

        # 5 拼音输入法候选（全拼/首字母/模糊拼音）
        py_seq, py_initials = normalize_to_pinyin(word)
        if py_seq != py_initials:
            candidates.extend(generate_from_pinyin(py_seq, static_dict=self.pinyin_to_words, candidates=added))
            candidates.extend(generate_from_pinyin(py_initials, static_dict=self.pinyin_to_words, candidates=added))
        else:
            candidates.extend(generate_from_pinyin(py_seq, static_dict=self.pinyin_to_words, candidates=added))
        candidates.extend(generate_by_fuzzy_pinyin(py_seq, self.pinyin_to_words, candidates=added))
        
        # 6 编辑距离近似词
        if should_use_edit_distance(word):
            dist_cands = generate_by_edit_distance(word, self.norm_vocab)
            for w in dist_cands:
                if w not in added:
                    candidates.append({"word": w, "source": "edit_distance"})
                    added.add(w)

        # 7 拼音序列seq2seq解码
        # candidates.update(generate_by_seq2seq(...))

        return self.sort_candidates(candidates)
    
    def sort_candidates(self, candidates):
        source_priority = {
            "original": 0,
            "static_dict": 1,
            "component": 2,
            "pinyin_static": 3,
            "pinyin_static_dict": 4,
            "pinyin": 5,
            "fuzzy_static_dict": 6,
            "fuzzy_pinyin": 7,
            "edit_distance": 8,
            "other": 99
        }

        unique = {}
        for cand in candidates:
            word = cand["word"]
            score = cand.get("confidence", 1.0)
            key = word
            if key not in unique:
                unique[key] = cand
            else:
                prev = unique[key]
                if source_priority.get(cand["source"], 99) < source_priority.get(prev["source"], 99):
                    unique[key] = cand
                elif score > prev.get("confidence", 1.0):
                    unique[key] = cand

        sorted_list = sorted(
            unique.values(),
            key=lambda x : (
                source_priority.get(x.get("source", "other"), 99),
                -x.get("confidence", 1.0)
            )
        )
        return [c["word"] for c in sorted_list]

    

if __name__ == "__main__":
    cg = CandidateGenerator()
    for test_word in ["bi", "gwi则", "弓虽", "doubi", "tm", "文刂"]:
        print(f"{test_word} => {cg.get_candidates(test_word)}")
