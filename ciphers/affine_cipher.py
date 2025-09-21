def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modInverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise ValueError(f"Modular inverse tidak ada untuk a={a}, m={m}. 'a' harus coprime dengan 26.")
    return x % m

def encrypt(data, key_str):
    if not isinstance(data, str): raise NotImplementedError("Affine Cipher hanya untuk teks.")
    try: a, b = map(int, key_str.split())
    except ValueError: raise ValueError("Kunci Affine harus berupa 2 angka dipisah spasi (contoh: '5 8').")
    
    result = ""
    for char in data.upper():
        if 'A' <= char <= 'Z':
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
    return result

def decrypt(data, key_str):
    if not isinstance(data, str): raise NotImplementedError("Affine Cipher hanya untuk teks.")
    try: a, b = map(int, key_str.split())
    except ValueError: raise ValueError("Kunci Affine harus berupa 2 angka dipisah spasi (contoh: '5 8').")
    
    a_inv = modInverse(a, 26)
    result = ""
    for char in data.upper():
        if 'A' <= char <= 'Z':
            result += chr((a_inv * ((ord(char) - 65) - b)) % 26 + 65)
    return result