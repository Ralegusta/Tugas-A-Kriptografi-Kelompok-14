import numpy as np
from .affine_cipher import modInverse

def create_matrix_from_key(key_str):
    try: nums = list(map(int, key_str.split()))
    except ValueError: raise ValueError("Kunci Hill harus berupa angka yang dipisah spasi.")
    
    size = int(np.sqrt(len(nums)))
    if size * size != len(nums) or size not in [2, 3]:
        raise ValueError("Kunci Hill harus berjumlah 4 (2x2) atau 9 (3x3) angka.")
    return np.array(nums).reshape(size, size)

def matrix_mod_inverse(matrix):
    modulus = 26
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = modInverse(det % modulus, modulus)
    matrix_adjugate = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * matrix_adjugate) % modulus

def process_text(text, key_matrix, mode):
    size = len(key_matrix)
    text = "".join([c for c in text.upper() if 'A' <= c <= 'Z'])
    
    if len(text) % size != 0:
        text += 'X' * (size - len(text) % size)
        
    if mode == 'decrypt':
        key_matrix = matrix_mod_inverse(key_matrix)
    
    result = ""
    for i in range(0, len(text), size):
        vector = np.array([ord(c) - 65 for c in text[i:i+size]])
        transformed_vector = np.dot(key_matrix, vector) % 26
        result += "".join([chr(x + 65) for x in transformed_vector])
    return result

def encrypt(data, key_str):
    if not isinstance(data, str): raise NotImplementedError("Hill Cipher hanya untuk teks.")
    key_matrix = create_matrix_from_key(key_str)
    return process_text(data, key_matrix, 'encrypt')

def decrypt(data, key_str):
    if not isinstance(data, str): raise NotImplementedError("Hill Cipher hanya untuk teks.")
    key_matrix = create_matrix_from_key(key_str)
    return process_text(data, key_matrix, 'decrypt')