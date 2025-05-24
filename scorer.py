from transformers import GPT2LMHeadModel, BertTokenizer
import torch
import math

class GPT2Scorer:
    def __init__(self, model_name='uer/gpt2-chinese-cluecorpussmall', device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def score(self, sentence: str) -> float:
        inputs = self.tokenizer(sentence, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
        return -loss.item()  # 取负值，得分越高表示句子越自然

    
if __name__ == "__main__":
    scorer = GPT2Scorer()
    template = "你是个{}"
    candidates = ["豆比", "逗比", "都比", "陡壁"]
    results = []
    for cand in candidates:
        sentence = template.format(cand)
        score = scorer.score(sentence)
        results.append((sentence, score))
    
    results.sort(key=lambda x: x[1], reverse=True)  # 分数越高越自然
    print("候选句打分结果：")
    for s, score in results:
        print(f"{s}  ->  得分: {score:.4f}")
