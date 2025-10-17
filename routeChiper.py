import math

class RoteChiper:
    
    def metin_matrisi_olustur(self,metin, yatay_uzunluk, dolgu_karakteri='*'):
       
        metin_uzunlugu = len(metin)
        dikey_uzunluk = math.ceil(metin_uzunlugu / yatay_uzunluk)
        toplam_eleman_sayisi = dikey_uzunluk * yatay_uzunluk
        dolgu_sayisi = toplam_eleman_sayisi - metin_uzunlugu
        dolgulu_metin = metin + (dolgu_karakteri * dolgu_sayisi)
        
        matris = []
        for i in range(dikey_uzunluk):
            baslangic_index = i * yatay_uzunluk
            bitis_index = baslangic_index + yatay_uzunluk
            satir = list(dolgulu_metin[baslangic_index:bitis_index])
            matris.append(satir)
            
        return matris

    def spiral_sag_ust_baslangic(self,matris):
        
        if not matris or not matris[0]:
            return ""

        ust_satir = 0
        alt_satir = len(matris) - 1
        sol_sutun = 0
        sag_sutun = len(matris[0]) - 1

        sonuc = []

        while ust_satir <= alt_satir and sol_sutun <= sag_sutun:
            
            
            for j in range(sag_sutun, sol_sutun - 1, -1):
                sonuc.append(matris[ust_satir][j])
            ust_satir += 1

            
            if sol_sutun <= sag_sutun:
                for i in range(ust_satir, alt_satir + 1):
                    sonuc.append(matris[i][sol_sutun])
                sol_sutun += 1
            
        
            if ust_satir <= alt_satir:
                for j in range(sol_sutun, sag_sutun + 1):
                    sonuc.append(matris[alt_satir][j])
                alt_satir -= 1
            
        
            if sol_sutun <= sag_sutun:
                for i in range(alt_satir, ust_satir - 1, -1):
                    sonuc.append(matris[i][sag_sutun])
                sag_sutun -= 1
                
        return "".join(sonuc)


