class RailFence:
    def __init__(self):
        
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        
    def railFenceSifreleme(self, anahtar, metin):
        if anahtar <= 1:
            return metin  
        
        
        diziler = [[] for _ in range(anahtar)]# her satır için bir liste oluşturduk
        cycle = 2 * (anahtar - 1)
        
        for i, harf in enumerate(metin): #ilgili harfin hangi satıra ekleneceğini bulduk.
            t = i % cycle
            if t < anahtar:
                row = t
            else:
                row = cycle - t
            diziler[row].append(harf)
        
        sifrelenmis_metin = "".join("".join(satir) for satir in diziler) #dizilerdeki listeleri birleşitrdik
        return sifrelenmis_metin

