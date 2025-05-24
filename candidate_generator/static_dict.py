def load_static_dict(dict_path):
    '''
    读取静态规范化词典文件，返回字典对象。
    格式要求：每行一个词对，用空格分隔。
    '''
    static_dict = {}
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ' ' not in line:
                continue
            key, value = line.split(' ')
            key = key.replace('_', ' ')
            value = value.replace('_', ' ')
            static_dict[key] = value
    return static_dict