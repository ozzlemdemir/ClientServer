import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class SecureAES:
  

    def __init__(self, key: str):
        key_bytes = key.encode("utf-8")

        if len(key_bytes) not in (16, 24, 32):
            raise ValueError("AES anahtarı 16, 24 veya 32 byte olmalıdır.")

        self.key = key_bytes

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))

    
        return base64.b64encode(iv + ciphertext).decode("utf-8")

    def decrypt(self, b64_ciphertext: str) -> str:
        data = base64.b64decode(b64_ciphertext)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode("utf-8")
