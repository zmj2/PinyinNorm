import re
import pkuseg
from candidate_generator.component_map import load_component_dict

LETTER_BLOCK_RE = re.compile(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*')  # 拼音+空格块
PUNCT_RE = re.compile(r'[。，！？；：“”《》、,.!?]')
HANZI_BLOCK_RE = re.compile(r'[\u4e00-\u9fff]+')

seg = pkuseg.pkuseg()

try:
    component_dict = load_component_dict("candidate_generator/dict/component_map.txt")
    component_keys = set(component_dict.keys())
except:
    component_keys = set()

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]

        if ch.isspace():
            i += 1
            continue  # 跳过空格

        # 拼音块（字母+空格）
        m = LETTER_BLOCK_RE.match(text, i)
        if m:
            tokens.append(m.group().strip())
            i = m.end()
            continue
        
        # 尝试匹配偏旁组合（最长优先匹配，最大长度设为3）
        matched = False
        for l in [3, 2]:
            sub = text[i:i + l]
            if sub in component_keys:
                tokens.append(sub)
                i += l
                matched = True
                break
        if matched:
            continue

        # 中文块（交给 pkuseg）
        m = HANZI_BLOCK_RE.match(text, i)
        if m:
            segs = seg.cut(m.group())
            tokens.extend(segs)
            i = m.end()
            continue

        # 标点
        m = PUNCT_RE.match(text, i)
        if m:
            tokens.append(m.group())
            i = m.end()
            continue

        # 默认逐字符兜底
        tokens.append(text[i])
        i += 1

    return tokens


if __name__ == "__main__":
    text = "doubi 脸太 gwi则了！zgr太强。禾斗匕匕。"
    print("分词结果：", tokenize(text))
