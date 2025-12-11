class RSA_Manual:
    def __init__(self):
        self.p = 61
        self.q = 53
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 17
        self.d = pow(self.e, -1, self.phi)

    def encrypt(self, plaintext: str) -> list:
        return [pow(ord(c), self.e, self.n) for c in plaintext]

    def decrypt(self, ciphertext: list) -> str:
        return "".join(chr(pow(c, self.d, self.n)) for c in ciphertext)
