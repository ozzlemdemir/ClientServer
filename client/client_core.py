import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import sys
import os
import zipfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AES_Chiper import SecureAES
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
from DES_Chiper import SecureDES
from DES_Manuel import DES_Manual
from AES_Manuel import AES_Manual
from RSA_Manuel import RSA_Manual

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
    elif secilen_sifreleme == "RSA":
        from RSA_Chiper import SecureRSA
        rsa = SecureRSA()

        print("PUBLIC KEY:")
        print(rsa.get_public_key_str())

        print("\nPRIVATE KEY:")
        print(rsa.get_private_key_str())


        normal = entry_girdi.get().strip()

        encrypted_b64 = rsa.encrypt(normal)
        decrypted = rsa.decrypt(encrypted_b64)

        mesaj = (
            "(RSA)\n"
            f"ŞİFRELİ (BASE64): {encrypted_b64}\n"
            f"ÇÖZÜLMÜŞ: {decrypted}"
        )
        
    elif secilen_sifreleme == "DES(Manuel)":
        print("\n--- DES(Manuel) BLOĞUNA GİRDİ ---")

        anahtar = entry_anahtar.get().strip()
        normal = entry_girdi.get().strip()

        print(f"[DEBUG] Girilen Anahtar: {anahtar}")
        print(f"[DEBUG] Girilen Mesaj: {normal}")

        des = DES_Manual(anahtar)
        print("[DEBUG] DES_Manual sınıfı oluşturuldu")

        try:
            sifreli = des.encrypt(normal)
            print(f"[DEBUG] Şifrelenen veri: {sifreli}")

            desifre = des.decrypt(sifreli)
            print(f"[DEBUG] Çözülen veri: {desifre}")
        except Exception as e:
            print(f"[HATA] DES Manuel işleminde hata oluştu: {e}")
            mesaj = f"[HATA] DES Manuel hata: {e}"
            
            return {
                "status": "fail",
                "sifreleme": "DES(Manuel)",
                "core": mesaj
            }

        mesaj = (
            "(DES-MANUEL)\n"
            f"ŞİFRELİ: {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {desifre}"
        )

        print("[DEBUG] Return paketi hazırlanıyor...")

        return {
            "status": "success",
            "sifreleme": "DES (Manuel)",
            "sifreli": sifreli,
            "desifre": desifre,
            "core": mesaj
        }

    elif secilen_sifreleme == "AES(Manuel)":
        aes = AES_Manual(entry_anahtar.get().strip())

        normal = entry_girdi.get().strip()
        sifreli = aes.encrypt(normal)
        desifre = aes.decrypt(sifreli)

        mesaj = (
            "(AES-MANUEL)\n"
            f"ŞİFRELİ: {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {desifre}"
        )

        return {
            "status": "success",
            "sifreleme": "AES (Manuel)",
            "sifreli": sifreli,
            "desifre": desifre,
            "core": mesaj
        }


    elif secilen_sifreleme == "DES(Manuel)":
        des = DES_Manual(entry_anahtar.get().strip())

        normal = entry_girdi.get().strip()
        sifreli = des.encrypt(normal)
        desifre = des.decrypt(sifreli)

        mesaj = (
            "(DES-MANUEL)\n"
            f"ŞİFRELİ (BASE64): {sifreli}\n"
            f"ÇÖZÜLMÜŞ: {desifre}"
        )

        client_socket.send(mesaj.encode("utf-8"))
        mesaj_ekle("CLIENT", mesaj)
        
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