
# Chinese Text Normalization System

This project is an end-to-end system for normalizing informal, error-prone, or non-standard Chinese input, particularly for cases involving:

- Pinyin input (full pinyin, initials, fuzzy variants)
- Character substitutions (e.g. component combinations like `弓虽` → `强`)
- Typos or phonetic errors (e.g. `doubi` → `逗比`)
- Mixed input with emoji, symbols, or non-standard tokens

It is designed as an academic and practical system for analyzing and normalizing natural Chinese user input.

---

## 🧩 Key Features

- **Intelligent tokenization**: Custom tokenizer supports pinyin strings, initials, and component combinations, overcoming limitations of standard segmentation.
- **Modular candidate generation**: Combines rules, static dictionaries, component maps, pinyin models, and edit distance.
- **Language model scoring**: Uses a pretrained GPT2 Chinese model (`uer/gpt2-chinese-cluecorpussmall`) to rank sentence candidates by fluency.
- **Customizable pipeline**: Each module is replaceable or extensible — e.g. swap language model, dictionary, or scoring logic.

---

## 📂 Project Structure

```

project-root/
├── main.py                         # Entry point for normalization
├── normalize.py                   # Custom tokenizer
├── scorer.py                      # GPT-based scoring module
├── candidate\_generator/
│   ├── generator.py               # Unified candidate generation
│   ├── static\_dict.py             # Static normalization dictionary
│   ├── component\_map.py           # Component combination mapping
│   ├── edit\_distance.py           # Typo correction by Levenshtein
│   ├── fuzzy\_pinyin.py            # Fuzzy pinyin expansion
│   ├── pinyin\_input\_method.py     # Full and initial pinyin conversion
│   └── seq2seq\_model.py           # (Optional) Somiao-style input method
├── dict/
│   ├── 规范词典2000条.txt
│   └── component\_map.txt
├── requirements.txt
└── README.md

```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Copy Pinyin2Hanzi module

> This project depends on the [`Pinyin2Hanzi`](https://github.com/letiantian/Pinyin2Hanzi) library
> Please clone or copy the `Pinyin2Hanzi` folder into the project root.

```bash
git clone https://github.com/letiantian/Pinyin2Hanzi.git
cp -r Pinyin2Hanzi ./Pinyin2Hanzi
```

> Or download manually and ensure `Pinyin2Hanzi/` is in the same folder as `main.py`.

---

### 3. Run normalization

```bash
python main.py "doubi脸太gwi则了"
```

Expected output:

```
🔍 Tokens: ['doubi', '脸', '太', 'gwi则', '了']
✅ Best normalized result: 逗比脸太规则了
🔢 Score: -2.83
```

---

## ⚙️ Customization

* **Scoring model**: You can replace `GPT2Scorer` with a different language model (e.g. ChatGLM or MacBERT).
* **Dictionaries**: Expand or update `dict/规范词典2000条.txt` and `component_map.txt`.
* **Candidate sources**: The generator uses multiple heuristics, and new modules can be easily added.

---

## 📄 License

MIT License.

---

## 🙏 Acknowledgments

* [pkuseg](https://github.com/lancopku/pkuseg-python)
* [pypinyin](https://github.com/mozillazg/python-pinyin)
* [python-Levenshtein](https://github.com/ztane/python-Levenshtein)
* [transformers](https://github.com/huggingface/transformers)
* [UER GPT2 Chinese](https://huggingface.co/uer/gpt2-chinese-cluecorpussmall)

---

## 👤 Author

**Barry Chao**

Undergraduate Student in Artificial Intelligence

Xiamen University, China

* 📧 Email: [barryjoth@gmail.com](mailto:barryjoth@gmail.com)
* 🧠 WeChat: `zmj_418`



