import string

class SubstituionChiper:
   

    def __init__(self, anahtar):
       
        self.anahtar = anahtar
        self.tum_harfler = string.ascii_letters
        self.alfabe_uzunlugu = len(self.tum_harfler)
     
        self.sifreleme_haritasi = self._harita_olustur(self.anahtar)
        self.desifreleme_haritasi = self._harita_olustur(-self.anahtar)

    def _harita_olustur(self, kaydirma: int) -> dict:
      
        sifre_haritasi = {}
        for i in range(self.alfabe_uzunlugu):
            hedef_indeks = (i + kaydirma) % self.alfabe_uzunlugu
            sifre_haritasi[self.tum_harfler[i]] = self.tum_harfler[hedef_indeks]
        return sifre_haritasi

    def sifrele(self, acik_metin: str) -> str:
  
        sifreli_metin_listesi = []
        for karakter in acik_metin:
            if karakter in self.sifreleme_haritasi:
                sifreli_metin_listesi.append(self.sifreleme_haritasi[karakter])
            else:
                sifreli_metin_listesi.append(karakter)

        return "".join(sifreli_metin_listesi)
    
