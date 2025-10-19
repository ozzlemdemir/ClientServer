import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sezar import Sezar
from vigenere import Vigenere
from railFence import RailFence
from routeChiper import RoteChiper
from substitutionChiper import SubstituionChiper
from playFair import PlayfairCipher
from affineChiper import AffineCipher

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
      mesaj = sezar.sezar_sifrele(entry_girdi.get().strip(),int(entry_anahtar.get())) #burada entry_anahtar ı aldık ve sezar dosyasındaki fonksiyona gönderdik
      
    elif secilen_sifreleme=="Vigenere":
        mesaj = vigenere.VigenereSifrele(entry_girdi.get().strip(),(entry_anahtar.get())) 
        
    elif secilen_sifreleme=="Rail Fence":
        mesaj=railFence.railFenceSifreleme(int(entry_anahtar.get()),entry_girdi.get().strip()) 
        
    elif secilen_sifreleme=="Route Chiper":
        matris=routeChiper.metin_matrisi_olustur(entry_girdi.get(),int(entry_anahtar.get())) 
        mesaj=routeChiper.spiral_sag_ust_baslangic(matris)
        
    elif secilen_sifreleme=="Substituion Chiper":
        anahtar = int(entry_anahtar.get().strip())
        substituionChiper=SubstituionChiper(anahtar)
        mesaj=substituionChiper.sifrele(entry_girdi.get()) 
    elif secilen_sifreleme=="Play Fair":
        anahtar=entry_anahtar.get()
        playfair=PlayfairCipher(anahtar)
        sifrelenecek=entry_girdi.get()
        mesaj=playfair.playfair_sifrele(sifrelenecek)
    elif secilen_sifreleme=="Affine":
        parcalar = entry_anahtar.get().split(',')
        a = int(parcalar[0].strip())
        b = int(parcalar[1].strip())
        affine=AffineCipher(a,b)
        mesaj=affine.encrypt(entry_girdi.get())
        
        
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