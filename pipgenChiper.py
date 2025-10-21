import os

class PipgenChiper:
    def __init__(self):
        # Görsellerin bulunduğu klasör
        self.image_dir = os.path.join(os.path.dirname(__file__), "images")

    def pipgen_sifrele(self, metin):
        """Metindeki harflere karşılık gelen resim dosya yollarını döndürür."""
        metin = metin.lower().replace(" ", "")
        resim_yollari = []

        for harf in metin:
            resim_yolu = os.path.join(self.image_dir, f"{harf}.png")
            if os.path.exists(resim_yolu):
                resim_yollari.append(resim_yolu)
            else:
                print(f"Uyarı: {harf} harfi için resim bulunamadı -> {resim_yolu}")

        return resim_yollari
