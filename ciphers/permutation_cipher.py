def process(data, key_map, block_size):
    padding_needed = (block_size - len(data) % block_size) % block_size
    if isinstance(data, str):
        data += 'X' * padding_needed
        result = ""
    else: # bytes
        data += b'\x00' * padding_needed
        result = b''
        
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        new_block = [block[j] for j in key_map]
        if isinstance(data, str): result += "".join(new_block)
        else: result += bytes(new_block)
    return result

def parse_key(key_str):
    try:
        if not key_str.isdigit(): raise ValueError
        block_size = len(key_str)
        key_map = [int(c) - 1 for c in key_str]
        if sorted(key_map) != list(range(block_size)):
            raise ValueError
        return key_map, block_size
    except ValueError:
        raise ValueError("Kunci Permutation tidak valid. Contoh: '312' untuk blok 3.")

def encrypt(data, key_str):
    key_map, block_size = parse_key(key_str)
    return process(data, key_map, block_size)

def decrypt(data, key_str):
    key_map, block_size = parse_key(key_str)
    inv_key_map = [0] * block_size
    for i, k in enumerate(key_map):
        inv_key_map[k] = i
    return process(data, inv_key_map, block_size)