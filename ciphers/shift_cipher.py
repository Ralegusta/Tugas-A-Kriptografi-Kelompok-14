def encrypt(data, key):
    key = int(key)
    if isinstance(data, str):  # Proses input teks
        result = ""
        for char in data.upper():
            if 'A' <= char <= 'Z':
                tesresult += chr(((ord(char) - 65 + key) % 26) + 65)
        return result
    elif isinstance(data, bytes):
        return bytes([(b + key) % 256 for b in data])

def decrypt(data, key):
    key = int(key)
    if isinstance(data, str): # Proses input teks
        result = ""
        for char in data.upper():
            if 'A' <= char <= 'Z':
                result += chr(((ord(char) - 65 - key) % 26) + 65)
        return result
    elif isinstance(data, bytes):
        return bytes([(b - key) % 256 for b in data])
    
