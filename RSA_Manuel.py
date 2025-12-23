import base64

class RSA_Manual:
    def __init__(self):
        # Basitlik için statik asal sayılar (Gerçekte çok daha büyük olmalı)
        self.p = 61
        self.q = 53
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 17
        self.d = self._mod_inverse(self.e, self.phi)

    def _mod_inverse(self, e, phi):
        """d = e^-1 mod phi hesaplaması (Kütüphanesiz)"""
        def gcd_extended(a, b):
            if a == 0: return b, 0, 1
            gcd, x1, y1 = gcd_extended(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = gcd_extended(e, phi)
        return (x % phi + phi) % phi

    def encrypt(self, plaintext: str) -> str:
        """Metni şifreler ve Base64 string döndürür."""
        # Her karakteri n modunda e kuvvetine yükselt
        cipher_list = [pow(ord(c), self.e, self.n) for c in plaintext]
        # Sayı listesini stringe çevirip Base64 ile paketle (İletim için)
        cipher_str = ",".join(map(str, cipher_list))
        return base64.b64encode(cipher_str.encode()).decode()

    def decrypt(self, ciphertext_b64: str) -> str:
        """Base64 string'i çözer ve orijinal metni döndürür."""
        try:
            # Base64'ten geri çevir ve virgülle ayrılmış sayıları al
            cipher_str = base64.b64decode(ciphertext_b64).decode()
            cipher_list = [int(c) for c in cipher_str.split(",")]
            # Her sayıyı n modunda d kuvvetine yükselt (Deşifre)
            return "".join(chr(pow(c, self.d, self.n)) for c in cipher_list)
        except:
            return "RSA Deşifre Hatası!"

    def get_public_key(self):
        return (self.n, self.e)

    def get_private_key(self):
        return (self.n, self.d)