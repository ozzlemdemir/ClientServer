
class Vigenere:
    
    def __init__(self):
        
        self.alphabet = [
            'a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h',
            'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p',
            'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z'
        ]
        self.alphabetLenght = len(self.alphabet)
        #alfabeyi sayisal degerlere çevirir
        self.char_to_int = {harf: index+1 for index, harf in enumerate(self.alphabet)}
        #sayisal degerleri alfabeye çevirir
        self.int_to_char = {index+1: harf for index, harf in enumerate(self.alphabet)}


    def harf_degeri(self, harf):
        harf_kucuk = harf.lower()
        return self.char_to_int.get(harf_kucuk, None)

    def degerden_harf(self, deger):
        modlu_deger = deger % self.alphabetLenght
        if modlu_deger == 0:
            modlu_deger = self.alphabetLenght
        return self.int_to_char.get(modlu_deger, None)
    
    def anahtar(self,anahtar):
        sayisal_anahtar=[]
        anahtar_kucuk=anahtar.lower()
        for harf in anahtar_kucuk:
            deger = self.harf_degeri(harf)
            sayisal_anahtar.append(deger)
        return sayisal_anahtar

        
        
    def VigenereSifrele(self,sifresiz_metin,anahtar_kelime):
        anahtar_sayisal=self.anahtar(anahtar_kelime)
        anahtar_uzunluk = len(anahtar_sayisal)
        sifreli_metin = ""
        anahtar_indeksi = 0
        sayısal_degerler=[]
        sifresiz_metin_kucuk=sifresiz_metin.lower()
        for harf in sifresiz_metin_kucuk:
            harf_degeri = self.harf_degeri(harf)
            if harf_degeri is not None:
                #metin boyu anahtar boyunu geçtiğinde başa döner
                anahtar_degeri = anahtar_sayisal[anahtar_indeksi % anahtar_uzunluk]
                 #alfabenin boyunu geçen değerleri garanti altına aldık mod ile
                sifreli_deger = (harf_degeri + anahtar_degeri) % self.alphabetLenght
                if sifreli_deger == 0:
                    sifreli_deger = self.alphabetLenght
                sifreli_harf = self.int_to_char[sifreli_deger]
                anahtar_indeksi += 1
            else:
                sifreli_harf = harf
            sifreli_metin += sifreli_harf
        return sifreli_metin
    


