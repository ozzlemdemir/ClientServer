class Sezar:
    encrypted_message = ''  # şifrelenmiş mesajı tutar
    decrypted_message = ''  # şifresi çözülmüş mesajı tutar

    def __init__(self):
        self.alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                         'o','p','r','s','t','u','v','y','z']

    
    def sezar_sifrele(self,decrypted_message, anahtar):
        sifreli_mesaj = ''
        for i in decrypted_message:
            sifreli_mesaj += self.alphabet[(self.alphabet.index(i) + anahtar) % len(self.alphabet)]
        return sifreli_mesaj

    @staticmethod
    def sezar_coz(self,encrypted_message, anahtar):
        sifresiz_mesaj = ''
        for i in encrypted_message:
            sifresiz_mesaj += self.alphabet[(self.alphabet.index(i) - anahtar) % len(self.alphabet)]
        return sifresiz_mesaj
