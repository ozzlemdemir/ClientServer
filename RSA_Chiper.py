from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

class SecureRSA:
    def __init__(self, public_key_path=None, private_key_path=None):
        self.public_key = None
        self.private_key = None

        # Eğer özel anahtar yolu verilmişse (Sunucu için)
        if private_key_path and os.path.exists(private_key_path):
            self.private_key = RSA.import_key(open(private_key_path, "rb").read())
            self.public_key = self.private_key.publickey()
            self.decryptor = PKCS1_OAEP.new(self.private_key)
            self.encryptor = PKCS1_OAEP.new(self.public_key)

        # Eğer sadece genel anahtar yolu verilmişse (İstemci için)
        elif public_key_path and os.path.exists(public_key_path):
            self.public_key = RSA.import_key(open(public_key_path, "rb").read())
            self.encryptor = PKCS1_OAEP.new(self.public_key)

    @staticmethod
    def generate_and_save_keys(server_folder, client_folder, key_size=2048):
        """Anahtarları bir kez üretir ve ilgili klasörlere kaydeder."""
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        # Sunucu klasörüne hem private hem public kaydedilir
        with open(os.path.join(server_folder, "server_private.pem"), "wb") as f:
            f.write(private_key)
        
        # İstemci klasörüne sadece public kaydedilir
        with open(os.path.join(client_folder, "server_public.pem"), "wb") as f:
            f.write(public_key)
        
        print("Anahtarlar başarıyla üretildi ve klasörlere dağıtıldı.")

    def encrypt(self, plaintext: str) -> str:
        if not self.public_key:
            return "HATA: Public Key yüklü değil!"
        ciphertext = self.encryptor.encrypt(plaintext.encode("utf-8"))
        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt(self, b64_ciphertext: str) -> str:
        if not self.private_key:
            return "HATA: Private Key yüklü değil!"
        ciphertext = base64.b64decode(b64_ciphertext)
        plaintext = self.decryptor.decrypt(ciphertext)
        return plaintext.decode("utf-8")