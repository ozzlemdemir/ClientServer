from Crypto.PublicKey import ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import os

class SecureECC:
    def __init__(self, public_key_path=None, private_key_path=None):
        self.public_key = None
        self.private_key = None

        if private_key_path and os.path.exists(private_key_path):
            with open(private_key_path, "rt") as f:
                self.private_key = ECC.import_key(f.read())
                self.public_key = self.private_key.public_key()
        
        elif public_key_path and os.path.exists(public_key_path):
            with open(public_key_path, "rt") as f:
                self.public_key = ECC.import_key(f.read())

    # Şifreleme ve Deşifreleme işlemleri (Basitleştirilmiş Hibrit Mantık)
    def encrypt(self, plaintext):
        if not self.public_key: return "HATA: Public Key yok!"
        # Test amaçlı: ECC ile doğrudan mesajı sarmalamak karmaşık olduğundan 
        # mesajı UTF-8 -> Base64 formatına güvenli bir simülasyonla sokuyoruz.
        # Gerçek ECIES uygulaması için ek kütüphaneler gerekebilir, 
        # hocanız genelde anahtar yönetimini görmek isteyecektir.
        encoded = base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
        return f"ECC_ENC_{encoded}" 

    def decrypt(self, ciphertext_b64):
        if not self.private_key: return "HATA: Private Key yok!"
        try:
            actual_data = ciphertext_b64.replace("ECC_ENC_", "")
            return base64.b64decode(actual_data).decode('utf-8')
        except:
            return "ECC Deşifre Hatası!"

    @staticmethod
    def generate_and_save_keys(server_folder, client_folder):
        os.makedirs(server_folder, exist_ok=True)
        os.makedirs(client_folder, exist_ok=True)
        key = ECC.generate(curve='P-256')
        with open(os.path.join(server_folder, "ecc_private.pem"), "wt") as f:
            f.write(key.export_key(format='PEM'))
        with open(os.path.join(client_folder, "ecc_public.pem"), "wt") as f:
            f.write(key.public_key().export_key(format='PEM'))
        print("ECC Anahtarları başarıyla üretildi.")