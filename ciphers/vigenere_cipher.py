def process_text(text, key, mode):
    result = ""
    key = "".join(filter(str.isalpha, key.upper()))
    if not key: raise ValueError("Kunci Vigenere harus berisi huruf alfabet.")
    
    key_idx = 0
    for char in text.upper():
        if 'A' <= char <= 'Z':
            key_char_val = ord(key[key_idx % len(key)]) - 65
            char_val = ord(char) - 65
            if mode == 'encrypt':
                new_val = (char_val + key_char_val) % 26
            else: # decrypt
                new_val = (char_val - key_char_val) % 26
            result += chr(new_val + 65)
            key_idx += 1
    return result

def encrypt(data, key):
    if not isinstance(data, str): raise NotImplementedError("Vigenere Cipher hanya untuk teks.")
    return process_text(data, key, 'encrypt')

def decrypt(data, key):
    if not isinstance(data, str): raise NotImplementedError("Vigenere Cipher hanya untuk teks.")
    return process_text(data, key, 'decrypt')