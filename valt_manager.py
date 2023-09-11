'''
Gère le chiffrement/déchifrement des mots de passes dans le vault en AES-256-CBC
'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

# Define a function to generate a random AES key
def random_AES_key():
    return get_random_bytes(32)  

# Define the encryption function
def encrypt_AES_CBC_256(key, message):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext_bytes = cipher.encrypt(padded_message)
    ciphertext = b64encode(iv + ciphertext_bytes).decode('utf-8')
    return ciphertext

# Define the decryption function
def decrypt_AES_CBC_256(key, ciphertext):
    ciphertext_bytes = b64decode(ciphertext)
    iv = ciphertext_bytes[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_bytes = ciphertext_bytes[AES.block_size:]
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    plaintext_bytes = unpad(decrypted_bytes, AES.block_size)
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext


