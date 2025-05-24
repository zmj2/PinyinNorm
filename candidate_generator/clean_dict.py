def clean_dict_file(input_path='dict/规范词典2000条_clean.txt',
                    clean_path='dict/规范词典2000条_clean2.txt',
                    irregular_path='dict/不规范行.txt'):
    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(clean_path, 'w', encoding='utf-8') as fout_clean, \
         open(irregular_path, 'w', encoding='utf-8') as fout_bad:

        for line in fin:
            line = line.strip()
            if not line:
                continue

            parts = line.split(' ')

            if len(parts) == 2:
                fout_clean.write(line + '\n')
            else:
                fout_bad.write(line + '\n')

    print(f"✅ 清洗完成：已输出规范行到 {clean_path}，不规范行共 {sum(1 for _ in open(irregular_path, encoding='utf-8'))} 行")

if __name__ == "__main__":
    clean_dict_file()
