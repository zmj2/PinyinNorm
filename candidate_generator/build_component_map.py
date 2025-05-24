import json

def build_component_map_from_makemehanzi(input_path="dict/dictionary.txt", output_path="dict/component_map.txt"):
    component_map = {}
    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            data = json.loads(line.strip())
            char = data.get('character')
            decomposition = data.get('decomposition')
            if decomposition and decomposition.startswith('⿰'):
                parts = decomposition[1:]
                parts = ''.join([p for p in parts if '\u4e00' <= p <= '\u9fff'])
                if len(parts) >= 2:
                    component_map[parts] = char
                    fout.write(f"{parts} {char}\n")
    print(f"✅ 构建完成，共收录 {len(component_map)} 项合字组合。保存于 {output_path}")


if __name__ == "__main__":
    build_component_map_from_makemehanzi()