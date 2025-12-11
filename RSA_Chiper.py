from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class SecureRSA:
    def __init__(self, key_size=2048):
       
        key = RSA.generate(key_size)
        self.private_key = key
        self.public_key = key.publickey()

        self.encryptor = PKCS1_OAEP.new(self.public_key)
        self.decryptor = PKCS1_OAEP.new(self.private_key)

    def encrypt(self, plaintext: str) -> str:
        ciphertext = self.encryptor.encrypt(plaintext.encode("utf-8"))
        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt(self, b64_ciphertext: str) -> str:
        ciphertext = base64.b64decode(b64_ciphertext)
        plaintext = self.decryptor.decrypt(ciphertext)
        return plaintext.decode("utf-8")
    def get_public_key_str(self):
        return self.public_key.export_key().decode()

    def get_private_key_str(self):
        return self.private_key.export_key().decode()
   
