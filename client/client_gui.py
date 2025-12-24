import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import sys
import client_core as Client



class ClientGUI:
    root = tk.Tk()
    root.title("Python Chat Client")

    label_sifreleme = tk.Label(root, text="Şifreleme Yöntemi Seçin:")
    label_sifreleme.pack()
    combo = ttk.Combobox(root, values=["Sezar", "Normal","Vigenere","Rail Fence","Route Chiper","Substituion Chiper",
                                       "Play Fair","Affine","Polybius Chiper","Pipgen Chiper",
                                       "Hill Chiper","DES","AES","RSA(Anahtar Dağitimi)","DES(Manuel)",
                                       "AES(Manuel)","RSA(Manuel)","ECC", "RSA(Mesaj Şifreleme)"], state="readonly")
    combo.current(0)  #varsayılan :Sezar
    combo.pack()

    label_anahtar = tk.Label(root, text="Anahtar girin : ")
    label_anahtar.pack()

    entry_anahtar = tk.Entry(root, width=20)
    entry_anahtar.pack()

    mesaj_alani = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=50)
    mesaj_alani.pack(padx=10, pady=10)

   
    input_frame = tk.Frame(root)
    input_frame.pack(padx=10, pady=(0, 10))
    label_bilgi = tk.Label(root, text="⚠️ Dosya seçmeden önce mutlaka anahtarınızı giriniz!", fg="red", font=("Arial", 9, "italic"))
    label_bilgi.pack(pady=(10, 0))
    btn_dosya = tk.Button(root, text="Dosya Şifrele ve Gönder", 
                     command=Client.dosya_sifrele_ve_gonder, 
                     bg="lightblue")
    btn_dosya.pack(pady=5)

    
    entry_girdi = tk.Entry(input_frame, width=40)
    entry_girdi.pack(side=tk.LEFT, padx=(0, 5))

    
    btn_gonder = tk.Button(input_frame, text="Gönder", command=Client.mesaj_gonder, state=tk.DISABLED)
    btn_gonder.pack(side=tk.LEFT)

    
    btn_baglan = tk.Button(root, text="SERVER'A BAĞLAN", command=lambda: threading.Thread(target=Client.baglan_ve_dinle, daemon=True).start())
    btn_baglan.pack(pady=(0, 10))

    
    root.bind('<Return>', lambda event: Client.mesaj_gonder())

    #TKİNTER ARAYÜZİNDEKİ WIDGETLARI CLIENT TARAFINDA KULLANMAK İÇİN
    Client.mesaj_alani = mesaj_alani
    Client.entry_girdi = entry_girdi
    Client.btn_baglan = btn_baglan
    Client.btn_gonder = btn_gonder
    Client.root = root
    Client.combo = combo
    Client.entry_anahtar = entry_anahtar
    Client.btn_dosya = btn_dosya


    root.mainloop()