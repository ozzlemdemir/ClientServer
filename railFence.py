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
    def railFenceDesifre(self, anahtar, sifreli_metin):
        if anahtar <= 1:
            return sifreli_metin

        uzunluk = len(sifreli_metin)
        cycle = 2 * (anahtar - 1)

        # Zigzag modeline göre her harfin gideceği satır (row) bilgisi hesaplanır
        row_index = []
        for i in range(uzunluk):
            t = i % cycle
            if t < anahtar:
                row = t
            else:
                row = cycle - t
            row_index.append(row)

        # Her satırın (row) kaç harften oluşacağını hesapla
        row_counts = [row_index.count(r) for r in range(anahtar)]

        # Şifreli metni satırlara böl
        rows = []
        idx = 0
        for count in row_counts:
            rows.append(list(sifreli_metin[idx:idx + count]))
            idx += count

        # Şimdi zigzag sırasına göre çözümü oluşturuyoruz
        pointers = [0] * anahtar
        cozulen_metin = []

        for r in row_index:
            cozulen_metin.append(rows[r][pointers[r]])
            pointers[r] += 1

        return "".join(cozulen_metin)

