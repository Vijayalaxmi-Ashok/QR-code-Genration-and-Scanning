
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64

# Generate a 32-byte AES key from the user's input (SHA-256)
def get_valid_key(user_key):
    return hashlib.sha256(user_key.encode('utf-8')).digest()  # SHA-256 -> 32 bytes

# Encrypt the message
def encrypt_message(message, key):
    key = get_valid_key(key)  # Ensure valid key length
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Ensure the message is in bytes and properly padded for encryption
    message_bytes = message.encode('utf-8')
    ct_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))
    
    # Combine IV and encrypted message for storage (base64 encoding for safe transfer)
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    
    return iv + ct  # Returning the combined data

# Decrypt the message
def decrypt_message(encrypted_message, key):
    key = get_valid_key(key)  # Ensure valid key length
    
    # Extract IV and cipher text
    iv = base64.b64decode(encrypted_message[:24])  # IV is the first 24 characters (base64 encoded)
    ct = base64.b64decode(encrypted_message[24:])  # Cipher text comes after the IV
    
    # Perform decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    
    return decrypted

