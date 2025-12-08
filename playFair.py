import string

class PlayfairCipher:
    
    def __init__(self, key):
        self.key = key
        self.square = self.matris_olustur(key)

    def matris_olustur(self, key):
        key = "".join([c.upper() for c in key if c.isalpha()])
        key = key.replace("J", "I")
        seen = set()
        square = []
    
        for c in key + string.ascii_uppercase:
            if c not in seen and c != "J":
                seen.add(c)
                square.append(c)
                
        return [square[i * 5 : (i + 1) * 5] for i in range(5)]
    
    def konumu_bul(self, char):
        
        for i, row in enumerate(self.square):
            if char in row:
                return i, row.index(char)
        return None

    def sifrelenecek_metin(self, text):
       
        text = "".join([c.upper() for c in text if c.isalpha()])
        text = text.replace("J", "I")
        result = ""
        i = 0
        
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else "X" 
            
            if a == b: 
                result += a + "X"
                i += 1
            else: 
                result += a + b
                i += 2
        if len(result) % 2 != 0: 
            result += "X"
            
        return result

    def playfair_sifrele(self, plaintext):
    
        text = self.sifrelenecek_metin(plaintext)
        result = ""
        
        for i in range(0, len(text), 2):
            a, b = text[i], text[i + 1]
            pos1 = self.konumu_bul(a)
            pos2 = self.konumu_bul(b)
            
            if pos1 is None or pos2 is None:
                raise ValueError(
                    f"Şifreleme hatası: '{a}' veya '{b}' karakteri Playfair matrisinde bulunamadı. "
                    "Lütfen metninizin sadece A-Z harfleri içerdiğinden emin olun."
                )
            r1, c1 = pos1
            r2, c2 = pos2
            
            if r1 == r2:
                result += self.square[r1][(c1 + 1) % 5] + self.square[r2][(c2 + 1) % 5]
            
            elif c1 == c2:
                result += self.square[(r1 + 1) % 5][c1] + self.square[(r2 + 1) % 5][c2]

            else:
                result += self.square[r1][c2] + self.square[r2][c1]
                
        return result

    def playfair_desifrele(self, ciphertext):
        result = ""

        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i + 1]
            pos1 = self.konumu_bul(a)
            pos2 = self.konumu_bul(b)

            if pos1 is None or pos2 is None:
                raise ValueError(
                    f"Deşifreleme hatası: '{a}' veya '{b}' Playfair matrisinde bulunamadı."
                )

            r1, c1 = pos1
            r2, c2 = pos2

            # Aynı satır: sola kaydır
            if r1 == r2:
                result += self.square[r1][(c1 - 1) % 5] + self.square[r2][(c2 - 1) % 5]

            # Aynı sütun: yukarı kaydır
            elif c1 == c2:
                result += self.square[(r1 - 1) % 5][c1] + self.square[(r2 - 1) % 5][c2]

            # Dikdörtgen: köşe değişimi (şifrelemenin tam tersi DEĞİL, aynı işlem!)
            else:
                result += self.square[r1][c2] + self.square[r2][c1]

        return result
