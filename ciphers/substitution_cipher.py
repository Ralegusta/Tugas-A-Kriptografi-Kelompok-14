ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(data, key):
    if not isinstance(data, str): raise NotImplementedError("Substitution Cipher hanya untuk teks.")
    key = key.upper()
    if len(key) != 26 or len(set(key)) != 26: raise ValueError("Kunci Substitution harus 26 huruf alfabet unik.")
    
    result = ""
    for char in data.upper():
        if char in ALPHABET:
            result += key[ALPHABET.find(char)]
    return result

def decrypt(data, key):
    if not isinstance(data, str): raise NotImplementedError("Substitution Cipher hanya untuk teks.")
    key = key.upper()
    if len(key) != 26 or len(set(key)) != 26: raise ValueError("Kunci Substitution harus 26 huruf alfabet unik.")

    result = ""
    for char in data.upper():
        if char in key:
            result += ALPHABET[key.find(char)]
    return result