from normalize import tokenize
from candidate_generator.generator import CandidateGenerator
from scorer import GPT2Scorer

from itertools import product
import sys
import math

def truncate_candidate_lists(candidate_lists, threshold):
    n = len(candidate_lists)
    if n == 0:
        return []

    max_k = int(threshold ** (1 / n))

    truncated = [clist[:max_k] for clist in candidate_lists]
    return truncated

def normalize_sentence(sentence, candidate_generator, scorer, topk=5, max_comb=100):
    tokens = tokenize(sentence)
    print("🔍 分词结果：", tokens)

    candidate_lists = []
    print("\n🎯 候选结果（按优先级排序）：")
    for token in tokens:
        cands = candidate_generator.get_candidates(token)
        print(f"{token} => {cands}")
        if not cands:
            cands = [token]
        candidate_lists.append(cands)

    total_comb = 1
    for c in candidate_lists:
        total_comb *= len(c)
    if total_comb > max_comb:
        print(f"\n⚠️ 候选组合过多（{total_comb}），已截断部分候选以提升性能")
        candidate_lists = truncate_candidate_lists(candidate_lists, threshold=max_comb)

    all_sentences = [''.join(words) for words in product(*candidate_lists)]

    scored = [(s, scorer.score(s)) for s in all_sentences]
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:topk]

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("📥 用法: python main.py '输入句子'")
        sys.exit(0)

    raw_input = sys.argv[1]

    print("🛠️ 正在加载候选生成器和语言模型...")
    generator = CandidateGenerator()
    scorer = GPT2Scorer()

    result = normalize_sentence(raw_input, generator, scorer)
    print("\n📌 相对最优输出结果：")
    print(result)

    print("\n✅ 最佳规范化结果：", result[0][0])
    print("🔢 得分：", result[0][1])

