import hashlib 
def encrypt(str2hash):
    return hashlib.md5(str2hash.encode()).hexdigest()