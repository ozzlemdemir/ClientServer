import base64

class DES_Manual:
    def __init__(self, key: str):
        self.key = key

    def xor_str(self, text, key):
        result = []
        for t, k in zip(text, key):
            result.append(chr(ord(t) ^ ord(k)))
        return "".join(result)

    def encrypt(self, plaintext: str) -> str:
        text = plaintext

        # Pad
        if len(text) % 2 != 0:
            text += " "

        h = len(text) // 2
        left, right = text[:h], text[h:]

        for _ in range(4):
            f = self.xor_str(right, self.key)
            left, right = right, f

        # SONUÇ → güvenli hâle getir (BASE64)
        raw = (left + right).encode("latin-1")
        return base64.b64encode(raw).decode("utf-8")

    def decrypt(self, ciphertext_b64: str) -> str:
        raw = base64.b64decode(ciphertext_b64)
        text = raw.decode("latin-1")

        h = len(text) // 2
        left, right = text[:h], text[h:]

        for _ in range(4):
            f = self.xor_str(left, self.key)
            left, right = right, f

        return (left + right).rstrip()
