def modular_inverse(a, m):

    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

class AffineCipher:
 
    ALPHABET_SIZE = 26  

    def __init__(self, a, b):
     
        if self._gcd(a, self.ALPHABET_SIZE) != 1:
            raise ValueError(f"Hata: 'a' ({a}) ve 26 aralarında asal olmalıdır. Lütfen başka bir 'a' değeri seçin.")

        self.a = a
        self.b = b
 
        self.a_inverse = modular_inverse(a, self.ALPHABET_SIZE)
        
        if self.a_inverse is None:
            raise ValueError("Hata: 'a' için modüler ters bulunamadı.")
 
        self.char_to_int = {chr(i + ord('A')): i for i in range(self.ALPHABET_SIZE)}
        self.int_to_char = {i: chr(i + ord('A')) for i in range(self.ALPHABET_SIZE)}

    def _gcd(self, x, y):
        while y:
            x, y = y, x % y
        return x

    def encrypt(self, plaintext):
       
        ciphertext = ""
        plaintext = "".join(filter(str.isalpha, plaintext.upper())) 
        
        for char in plaintext:
            if char in self.char_to_int:
                x = self.char_to_int[char]
                y = (self.a * x + self.b) % self.ALPHABET_SIZE
                ciphertext += self.int_to_char[y]
            else:
                ciphertext += char 
                
        return ciphertext

    