import re
import jieba

LETTER_BLOCK_RE = re.compile(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*')
PUNCT_RE = re.compile(r'[。，！？；：“”《》、,.!?]')
HANZI_BLOCK_RE = re.compile(r'[\u4e00-\u9fff]+')

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]
        
        if ch.isspace():
            i += 1
            continue

        m = LETTER_BLOCK_RE.match(text, i)
        if m:
            tokens.append(m.group().strip())
            i = m.end()
            continue

        m = HANZI_BLOCK_RE.match(text, i)
        if m:
            tokens.extend(list(jieba.cut(m.group())))
            i = m.end()
            continue

        m = PUNCT_RE.match(text, i)
        if m:
            tokens.append(m.group())
            i = m.end()
            continue

        tokens.append(ch)
        i += 1

    return tokens

if __name__ == "__main__":
    text = "doubi 脸太 dou bi后悔！zgr太强"
    print("分词结果：", tokenize(text))
