class HillCipher:
    def __init__(self, key_string, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
       
        self.alphabet = alphabet
        self.m = len(alphabet)
        self.char_to_idx = {c: i for i, c in enumerate(alphabet)}
        self.idx_to_char = {i: c for i, c in enumerate(alphabet)}

        nums = [int(x.strip()) for x in key_string.split(",") if x.strip() != ""]
        import math
        k = int(math.isqrt(len(nums)))
        if k * k != len(nums):
            raise ValueError("Anahtar uzunluğu kare değil!")
        self.n = k
        self.key = [nums[i*self.n:(i+1)*self.n] for i in range(self.n)]

    def _clean_text(self, text):
        text = text.upper()
        text = "".join([c for c in text if c in self.char_to_idx])
        pad_char = 'X' if 'X' in self.char_to_idx else self.idx_to_char[self.m - 1]
        while len(text) % self.n != 0:
            text += pad_char
        return text

    def _encrypt_block(self, block):
        vec = [self.char_to_idx[c] for c in block]
        res = [sum(self.key[i][j] * vec[j] for j in range(self.n)) % self.m for i in range(self.n)]
        return "".join(self.idx_to_char[v] for v in res)

    def encrypt(self, plaintext):
        text = self._clean_text(plaintext)
        blocks = [text[i:i+self.n] for i in range(0, len(text), self.n)]
        return "".join(self._encrypt_block(block) for block in blocks)
    
    
    def _mod_inverse_matrix(self, matrix):
        import numpy as np

        det = int(round(np.linalg.det(matrix)))
        det_mod = det % self.m

        det_inv = None
        for x in range(self.m):
            if (det_mod * x) % self.m == 1:
                det_inv = x
                break

        if det_inv is None:
            raise ValueError("Anahtar matrisinin determinantı modüler ters üretmiyor! Hill çözülemez.")

        matrix_np = np.array(matrix)
        adj = np.round(det * np.linalg.inv(matrix_np)).astype(int)

        inv_mod = (det_inv * adj) % self.m
        return inv_mod

    def _decrypt_block(self, block, inv_key):
        vec = [self.char_to_idx[c] for c in block]
        import numpy as np
        res = np.dot(inv_key, vec) % self.m
        return "".join(self.idx_to_char[int(v)] for v in res)

    def decrypt(self, ciphertext):
        import numpy as np

        text = "".join([c for c in ciphertext.upper() if c in self.char_to_idx])
        blocks = [text[i:i+self.n] for i in range(0, len(text), self.n)]

      
        inv_key = self._mod_inverse_matrix(self.key)

        result = ""
        for block in blocks:
            result += self._decrypt_block(block, inv_key)

        return result
