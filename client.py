import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import sys
from sezar import Sezar


host_input = input("Sunucu IP adresini girinnn (varsayılan: 127.0.0.1): ")
HOST = host_input if host_input else "127.0.0.1"

port_input = input("Sunucu port numarasını girin (varsayılan: 12345): ")
PORT = 0 

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
    """Client bağlantısını kurar ve mesaj dinleme iş parçacığını (thread) başlatır."""
    global client_socket

    try:
        client_socket = socket.socket()
        client_socket.connect((HOST, PORT))
        mesaj_ekle("BAĞLANTI", f"Server'a bağlandın: {HOST}:{PORT}")

        # Arka planda mesajları dinleme fonksiyonu çalıştır
        threading.Thread(target=mesajlari_dinle, daemon=True).start()

        # Arayüzdeki durumu güncelle
        btn_baglan.config(state=tk.DISABLED) # Bağlan butonunu pasifleştir
        btn_gonder.config(state=tk.NORMAL)   # Gönder butonunu aktifleştir

    except socket.error as e:
        mesaj_ekle("HATA", f"[Server aktif değil.] Hata: {e}")

def mesajlari_dinle():
    """Server'dan gelen mesajları sürekli dinler."""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                mesaj_ekle("BAĞLANTI", "Server bağlantıyı kapattı.")
                break
            mesaj_ekle("SERVER", data.decode("utf-8"))
        except:
            break # Bağlantı koparsa döngüyü sonlandır


def mesaj_gonder():
    """Giriş kutusundaki mesajı server'a gönderir."""
    sezar=Sezar()
    secilen_sifreleme = combo.get()
    if secilen_sifreleme=="Sezar":
      mesaj = sezar.sezar_sifrele(entry_girdi.get().strip(),int(entry_anahtar.get()))#burada entry_anahtar ı aldık ve sezar dosyasındaki fonksiyona gönderdik
    else:
      mesaj = entry_girdi.get().strip()

    if mesaj:
        mesaj_ekle("SEN", mesaj)
        client_socket.send(mesaj.encode("utf-8"))
        entry_girdi.delete(0, tk.END) # Giriş kutusunu temizle

        if mesaj.lower() == "exit":
            client_socket.close()
            root.quit()

def mesaj_ekle(kaynak, metin):
    """Gelen/Giden mesajları ana mesaj alanına ekler."""
    mesaj_alani.config(state=tk.NORMAL) # Yazılabilir yap
    mesaj_alani.insert(tk.END, f"[{kaynak}]: {metin}\n")
    mesaj_alani.yview(tk.END) # En alta kaydır
    mesaj_alani.config(state=tk.DISABLED) # Salt okunur yap

# --- 2. Arayüz Tasarımı (Ana Pencere) ---

root = tk.Tk()
root.title("Python Chat Client")

# Mesaj Alanı

label_sifreleme = tk.Label(root, text="Şifreleme Yöntemi Seçin:")
label_sifreleme.pack()
combo = ttk.Combobox(root, values=["Sezar", "Normal"], state="readonly")
combo.current(0)  #varsayılan :Sezar
combo.pack()

label_anahtar = tk.Label(root, text="Anahtar girin : ")
label_anahtar.pack()

entry_anahtar = tk.Entry(root, width=20)
entry_anahtar.pack()

mesaj_alani = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=50)
mesaj_alani.pack(padx=10, pady=10)

# Giriş Kutusu ve Butonlar için Frame
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10))

# Mesaj Giriş Kutusu
entry_girdi = tk.Entry(input_frame, width=40)
entry_girdi.pack(side=tk.LEFT, padx=(0, 5))

# Gönder Butonu
btn_gonder = tk.Button(input_frame, text="Gönder", command=mesaj_gonder, state=tk.DISABLED)
btn_gonder.pack(side=tk.LEFT)

# Bağlan Butonu (Giriş kutusu ve butondan ayrı bir yerde)
btn_baglan = tk.Button(root, text="SERVER'A BAĞLAN", command=lambda: threading.Thread(target=baglan_ve_dinle, daemon=True).start())
btn_baglan.pack(pady=(0, 10))

# Enter tuşuna basıldığında mesaj gönderme işlevi ekle
root.bind('<Return>', lambda event: mesaj_gonder())

# --- 3. Uygulamayı Başlat ---

root.mainloop()