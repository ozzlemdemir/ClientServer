import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import sys
import os
import zipfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sezar import Sezar
from vigenere import Vigenere
from railFence import RailFence
from routeChiper import RoteChiper
from substitutionChiper import SubstituionChiper
from playFair import PlayfairCipher
from affineChiper import AffineCipher
from polybiusChiper import PolybiusChiper
from pipgenChiper import PipgenChiper
from hillChiper import HillCipher 
from AES_Chiper import SecureAES  
from DES_Chiper import SecureDES
from DES_Manuel import DESCipher
from AES_Manuel import SimpleAESCipher
from RSA_Manuel import RSA_Manual
from RSA_Chiper import SecureRSA
from ECC_Chiper import SecureECC
from tkinter import filedialog 
import docx


import base64

#client_core.py

host_input = input("Sunucu IP adresini girinnn (varsayılan: 127.0.0.1): ")
HOST = host_input if host_input else "127.0.0.1"

port_input = input("Sunucu port numarasını girin (varsayılan: 12345): ")
PORT = 0 
#arayuzden gelen alana atamak için global değişkenler
root = None
mesaj_alani = None
entry_girdi = None
btn_baglan = None
btn_gonder = None
combo = None
entry_anahtar = None
btn_dosya = None


if not port_input:
    PORT = 12345
else:
    try:
        # Tırnak işaretlerini (", ') ve boşlukları temizleyerek int'e çevir
        temiz_port = port_input.strip().strip('"').strip("'")
        PORT = int(temiz_port)
        
        if not (1024 <= PORT <= 65535):
            print("UYARI: Port numarası 1024 ile 65535 arasında olmalıdır. Varsayılan (12345) kullanılıyor.")
            PORT = 12345
            
    except ValueError:
        print(f"HATA: Port numarası ('{port_input}') geçerli bir sayı değil. Varsayılan (12345) kullanılıyor.")
        PORT = 12345


# --- 1. Arayüz Fonksiyonları ---

def baglan_ve_dinle():
    global client_socket

    try:
        client_socket = socket.socket()
        client_socket.connect((HOST, PORT))
        mesaj_ekle("BAĞLANTI", f"Server'a bağlandın: {HOST}:{PORT}")

        # Arka planda mesajları dinleme fonksiyonu çalıştır
        threading.Thread(target=mesajlari_dinle, daemon=True).start()

        btn_baglan.config(state=tk.DISABLED)
        btn_gonder.config(state=tk.NORMAL)  
    except socket.error as e:
        mesaj_ekle("HATA", f"[Server aktif değil.] Hata: {e}")

def mesajlari_dinle():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                mesaj_ekle("BAĞLANTI", "Server bağlantıyı kapattı.")
                break
            mesaj_ekle("SERVER", data.decode("utf-8"))
        except:
            break 
""

#sonradan eklenen dosya işleme kısmı
def dosya_sec_ve_oku():
    dosya_yolu = filedialog.askopenfilename(
        title="Şifrelenecek Dosyayı Seçin",
        filetypes=[("Text Dosyaları", "*.txt"), ("Word Dosyaları", "*.docx"), ("Tüm Dosyalar", "*.*")]
    )
    
    if not dosya_yolu:
        return None

    try:
        if dosya_yolu.endswith('.txt'):
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif dosya_yolu.endswith('.docx'):
            doc = docx.Document(dosya_yolu)
            tam_metin = [para.text for para in doc.paragraphs]
            return '\n'.join(tam_metin)
            
    except Exception as e:
        mesaj_ekle("HATA", f"Dosya okunurken hata oluştu: {e}")
        return None

def dosya_sifrele_ve_gonder():
    """Dosyadan okur, arayüzdeki yönteme göre şifreler ve gönderir."""
    dosya_metni = dosya_sec_ve_oku()
    
    if dosya_metni:
        # entry_girdi'ye geçici olarak dosya metnini yazıyoruz 
        # (mesaj_gonder fonksiyonunun mevcut yapısını bozmamak için en kolay yol budur)
        eski_mesaj = entry_girdi.get()
        entry_girdi.delete(0, tk.END)
        entry_girdi.insert(0, dosya_metni)
        
        # Mevcut şifreleme fonksiyonunuzu çağırın
        mesaj_gonder()
        
        # İşlem bitince kutuyu temizleyebilir veya eski mesajı geri koyabilirsiniz
        entry_girdi.delete(0, tk.END)
        entry_girdi.insert(0, eski_mesaj)
#sonradan eklenen kısmın sonu 

def mesaj_gonder():
    sezar=Sezar()
    vigenere=Vigenere()
    railFence=RailFence()
    routeChiper=RoteChiper()
    secilen_sifreleme = combo.get() 
    
    if secilen_sifreleme=="Sezar":
     normal = entry_girdi.get().strip()
     anahtar = int(entry_anahtar.get())

     encrypted = sezar.sezar_sifrele(normal, anahtar)
     decrypted = sezar.sezar_coz(encrypted, anahtar)

     mesaj = (
        "(SEZAR)\n"
        f"ŞİFRELİ: {encrypted}\n"
        f"ÇÖZÜLMÜŞ: {decrypted}"
    )
      
    elif secilen_sifreleme == "Vigenere":
        normal = entry_girdi.get().strip()
        key = entry_anahtar.get().strip()

        encrypted = vigenere.VigenereSifrele(normal, key)
        decrypted = vigenere.VigenereCoz(encrypted, key)

        mesaj = (
            "(VIGENERE)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        ) 
        
    elif secilen_sifreleme == "Rail Fence":
        normal = entry_girdi.get().strip()
        key = int(entry_anahtar.get().strip())

        encrypted = railFence.railFenceSifreleme(key, normal)
        decrypted = railFence.railFenceDesifre(key, encrypted)

        mesaj = (
            "(RAIL FENCE)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "Route Chiper":
        metin = entry_girdi.get().strip()
        key = int(entry_anahtar.get().strip())

        matris = routeChiper.metin_matrisi_olustur(metin, key)
        encrypted = routeChiper.spiral_sag_ust_baslangic(matris)
        decrypted = routeChiper.spiral_sag_ust_baslangic_coz(encrypted, key)

        mesaj = (
            "(ROUTE CHIPHER)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme=="Substituion Chiper":
        anahtar = int(entry_anahtar.get().strip())
        substituionChiper = SubstituionChiper(anahtar)

        encrypted = substituionChiper.sifrele(entry_girdi.get())
        decrypted = substituionChiper.desifrele(encrypted)

        mesaj = (
            "(SUBSTITUTION)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "Play Fair":
        anahtar = entry_anahtar.get().strip()
        playfair = PlayfairCipher(anahtar)

        normal = entry_girdi.get().strip()
        encrypted = playfair.playfair_sifrele(normal)
        decrypted = playfair.playfair_desifrele(encrypted)

        mesaj = (
            "(PLAYFAIR)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "Affine":
        try:
            parcalar = entry_anahtar.get().split(',')
            if len(parcalar) != 2:
                raise ValueError("Anahtarı 'a,b' formatında girin. Örn: 5,8")

            a = int(parcalar[0].strip())
            b = int(parcalar[1].strip())

            affine = AffineCipher(a, b)

            normal = entry_girdi.get().strip()
            encrypted = affine.encrypt(normal)
            decrypted = affine.decrypt(encrypted)

            mesaj = (
                "(AFFINE)\n"
                f"ŞİFRELİ: {encrypted}\n"
                f"ÇÖZÜLMÜŞ: {decrypted}"
            )

        except Exception as e:
            mesaj = f"[HATA] Affine anahtar hatası: {e}"
        
    elif secilen_sifreleme == "Polybius Chiper":
        polybius = PolybiusChiper()

        normal = entry_girdi.get().strip()

        encrypted = polybius.polybiusCipher(normal)
        decrypted = polybius.polybiusDeCipher(encrypted)

        mesaj = (
            "(POLYBIUS)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "Hill Chiper":
        hill = HillCipher(entry_anahtar.get().strip())

        normal = entry_girdi.get().strip()
        encrypted = hill.encrypt(normal)
        decrypted = hill.decrypt(encrypted)

        mesaj = (
            "(HILL)\n"
            f"ŞİFRELİ: {encrypted}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "DES":
        des = SecureDES(entry_anahtar.get().strip())

        normal = entry_girdi.get().strip()
        cipher_bytes = des.encrypt(normal)
        encrypted_b64 = base64.b64encode(cipher_bytes).decode("utf-8")
        decrypted = des.decrypt(cipher_bytes)

        mesaj = (
            "(DES)\n"
            f"ŞİFRELİ (BASE64): {encrypted_b64}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "AES":
        aes = SecureAES(entry_anahtar.get().strip())

        normal = entry_girdi.get().strip()

        # Şifrele (BASE64 olarak döner)
        encrypted_b64 = aes.encrypt(normal)

        # Çöz
        decrypted = aes.decrypt(encrypted_b64)
        
        mesaj = (
            "(AES)\n"
            f"ŞİFRELİ (BASE64): {encrypted_b64}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
    elif secilen_sifreleme == "RSA(Anahtar Dağitimi)":
        public_path = os.path.join("client", "server_public.pem")
        
        try:
            rsa_islem = SecureRSA(public_key_path=public_path)
            
            # Geçici AES anahtarı 
            import secrets
            gecici_aes_anahtari = secrets.token_hex(8) 
    
            aes_islem = SecureAES(gecici_aes_anahtari)
            sifreli_mesaj = aes_islem.encrypt(entry_girdi.get().strip())
            
            # 5. AES ANAHTARINI RSA ile şifrele (Anahtar Dağıtımı Burasıdır)
            sifreli_aes_key = rsa_islem.encrypt(gecici_aes_anahtari)
            
            # 6. Sunucuya gönderilecek birleşik paket
            mesaj = (
                "(RSA-KEY-EXCHANGE)\n"
                f"ŞİFRELİ_ANAHTAR: {sifreli_aes_key}\n"
                f"ŞİFRELİ_MESAJ: {sifreli_mesaj}"
            )
            
        except Exception as e:
            mesaj_ekle("HATA", f"RSA Anahtar Dağıtım Hatası: {e}")
            return
        
    elif secilen_sifreleme == "DES(Manuel)":
        des = DESCipher()

        normal = entry_girdi.get().strip()
        anahtar= entry_anahtar.get().strip()
        sifreli = des.encrypt(normal,anahtar)
        cözülmüş = des.decrypt(sifreli,anahtar)

        mesaj = (
            "(DES-MANUEL)\n"
            f"ŞİFRELİ (BASE64): {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {cözülmüş}"
            
        )

    elif secilen_sifreleme == "AES(Manuel)":
        aes=SimpleAESCipher(entry_anahtar.get().strip())
        sifreli=aes.encrypt(entry_girdi.get().strip())
        cözülmüş=aes.decrypt(sifreli)
        mesaj = (
            "(AES-MANUEL)\n"
            f"ŞİFRELİ (BASE64): {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {cözülmüş}"
        )
    
    elif secilen_sifreleme=="RSA(Manuel)":
        rsa=RSA_Manual()
        sifreli=rsa.encrypt(entry_girdi.get().strip())
        cözülmüş=rsa.decrypt(sifreli)
        mesaj = (
            "(RSA-MANUEL)\n"
            f"ŞİFRELİ (BASE64): {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {cözülmüş}"
        )
    elif secilen_sifreleme == "RSA(Mesaj Şifreleme)":
        public_path = os.path.join("client", "server_public.pem")
        private_path = os.path.join("server", "server_private.pem")
        
        try:
            rsa_islem = SecureRSA(public_key_path=public_path, private_key_path=private_path)
            
            normal_metin = entry_girdi.get().strip()
            if not normal_metin:
                mesaj_ekle("UYARI", "Lütfen bir mesaj girin.")
                return
            sifreli_mesaj = rsa_islem.encrypt(normal_metin)

            if rsa_islem.private_key:
                cozulmus_metin = rsa_islem.decrypt(sifreli_mesaj)
            else:
                cozulmus_metin = "[Özel Anahtar Yüklenemedi - Çözülemez]"

            mesaj = (
                "(RSA-DOĞRUDAN-ŞİFRELEME)\n"
                f"ŞİFRELİ (BASE64): {sifreli_mesaj}\n"
                f"ÇÖZÜLMÜŞ: {cozulmus_metin}"
            )
        except Exception as e:
            mesaj_ekle("HATA", f"RSA İşlemi başarısız: {e}")
            return
    elif secilen_sifreleme=="ECC":
        # Klasör yapılandırmana göre tam yollar:
        public_path = os.path.join("client", "ecc_public.pem")
        private_path = os.path.join("server", "ecc_private.pem")

        try:
            # Sınıfı başlatırken yolları veriyoruz
            ecc_islem = SecureECC(public_key_path=public_path, private_key_path=private_path)
            
            normal_metin = entry_girdi.get().strip()
            if not normal_metin:
                mesaj_ekle("UYARI", "Lütfen bir mesaj girin.")
                return

            # Şifreleme (Client tarafı)
            sifreli = ecc_islem.encrypt(normal_metin)
            
            # Deşifreleme (Test amaçlı Client tarafında yapıyoruz)
            # Normalde ecc_private.pem sadece serverda olur, 
            # ama şu an aynı bilgisayarda olduğun için client da okuyabiliyor.
            if ecc_islem.private_key:
                cozulmus = ecc_islem.decrypt(sifreli)
            else:
                cozulmus = "[Sadece Sunucu Çözebilir]"

            mesaj = (
                "(ECC)\n"
                f"ŞİFRELİ (BASE64): {sifreli}\n"
                f"ÇÖZÜLMÜŞ: {cozulmus}"
            )
        except Exception as e:
            mesaj_ekle("HATA", f"ECC İşlemi başarısız: {e}\nAranan Yol: {os.path.abspath(public_path)}")
            return
        
    elif secilen_sifreleme == "Pipgen Chiper":
        from PIL import Image, ImageTk  # type: ignore
        pipgen = PipgenChiper()
        yollar = pipgen.pipgen_sifrele(entry_girdi.get().strip())
   
        if not yollar:
            mesaj_ekle("UYARI", "Hiçbir harf için resim bulunamadı.")
            return

        zip_yolu = "pipgen_mesaj.zip"
        with zipfile.ZipFile(zip_yolu, "w") as zipf:
            for yol in yollar:
                zipf.write(yol, os.path.basename(yol))  # sadece dosya adını ekle

        mesaj_ekle("SEN", f"Pipgen mesajı dosyaya kaydedildi: {zip_yolu}")

        #sunucu tarafına gönderme
        with open(zip_yolu, "rb") as f:
            data = f.read()
            client_socket.sendall(b"[FILE]" + data)
        mesaj_ekle("BILGI", "Pipgen dosyası sunucuya gönderildi.")
        return
        
    else:
      mesaj = entry_girdi.get().strip()

    if mesaj:
        mesaj_ekle("SEN", mesaj)
        client_socket.send(mesaj.encode("utf-8"))
        entry_girdi.delete(0, tk.END)  # Giriş kutusunu temizle

        if mesaj.lower() == "exit":
            client_socket.close()
            root.quit() 

def mesaj_ekle(kaynak, metin):
    """Gelen/Giden mesajları ana mesaj alanına ekler."""
    mesaj_alani.config(state=tk.NORMAL) # Yazılabilir yap
    mesaj_alani.insert(tk.END, f"[{kaynak}]: {metin}\n") 
    mesaj_alani.yview(tk.END) # En alta kaydır
    mesaj_alani.config(state=tk.DISABLED)  # Salt okunur yap