def run():
    pass

def generate_charset_file(labels_file, charset_path):
    chars = set()
    with open(labels_file, 'r', encoding='utf-8') as f:
        for line in f:
            _, text = line.strip().split('\t')
            chars.update(text)

    with open(charset_path, 'w', encoding='utf-8') as f:
        for char in sorted(chars):
            f.write(f"{char}\n")
