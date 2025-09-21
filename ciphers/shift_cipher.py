def process_text(text, key, mode):
    result = ""
    for char in text.upper():
        if 'A' <= char <= 'Z':
            offset = ord(char) - 65
            new_offset = (offset + key) % 26 if mode == 'encrypt' else (offset - key) % 26
            result += chr(new_offset + 65)
    return result

def process_bytes(data, key, mode):
    key = key % 256
    if mode == 'encrypt':
        return bytes([(b + key) % 256 for b in data])
    return bytes([(b - key) % 256 for b in data])

def encrypt(data, key_str):
    try: key = int(key_str)
    except ValueError: raise ValueError("Kunci Shift Cipher harus berupa angka.")
    return process_bytes(data, key, 'encrypt') if isinstance(data, bytes) else process_text(data, key, 'encrypt')

def decrypt(data, key_str):
    try: key = int(key_str)
    except ValueError: raise ValueError("Kunci Shift Cipher harus berupa angka.")
    return process_bytes(data, key, 'decrypt') if isinstance(data, bytes) else process_text(data, key, 'decrypt')