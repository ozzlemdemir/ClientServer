class AES_Manual:
    def __init__(self, key: str):
        self.key = key

    def sub_bytes(self, text):
        return "".join(chr((ord(c) + 1) % 256) for c in text)

    def shift_rows(self, text):
        return text[1:] + text[0]

    def mix_columns(self, text):
        return "".join(chr(ord(c) ^ 0x12) for c in text)

    def add_round_key(self, text):
        out = ""
        for t, k in zip(text, self.key):
            out += chr(ord(t) ^ ord(k))
        return out

    def encrypt(self, plaintext: str) -> str:
        text = plaintext
        
        for _ in range(5): 
            text = self.sub_bytes(text)
            text = self.shift_rows(text)
            text = self.mix_columns(text)
            text = self.add_round_key(text)

        return text

    def decrypt(self, ciphertext: str) -> str:
        text = ciphertext

        for _ in range(5):
            text = self.add_round_key(text)
            text = self.mix_columns(text)
            text = self.shift_rows(text)
            text = self.sub_bytes(text)

        return text
