import os
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

class SecureDES:
   

    def __init__(self, key: str):
        key_bytes = key.encode("utf-8")
        if len(key_bytes) != 8:
            raise ValueError("DES anahtarı 8 byte olmalıdır.")
        self.key = key_bytes

    def encrypt(self, plaintext: str) -> bytes:
        iv = os.urandom(8)
        cipher = DES.new(self.key, DES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(plaintext.encode("utf-8"), 8))
        return iv + encrypted

    def decrypt(self, data: bytes) -> str:
        iv = data[:8]
        ciphertext = data[8:]
        cipher = DES.new(self.key, DES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), 8)
        return decrypted.decode("utf-8")
