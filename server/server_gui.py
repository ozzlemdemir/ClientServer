import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import sys
import server as Server

class ServerGUI:
    root = tk.Tk()
    root.title("Python Chat Server")
    root.protocol("WM_DELETE_WINDOW", Server.on_closing)

    mesaj_alani = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=60)
    mesaj_alani.pack(padx=10, pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(padx=10, pady=(0, 10))

    btn_start = tk.Button(button_frame, text="SERVER'I BAŞLAT", command=Server.start_server, fg="green")
    btn_start.pack(side=tk.LEFT, padx=5)

    btn_stop = tk.Button(button_frame, text="SERVER'I DURDUR", command=Server.stop_server, fg="red", state=tk.DISABLED)
    btn_stop.pack(side=tk.LEFT, padx=5)

    input_frame = tk.Frame(root)
    input_frame.pack(padx=10, pady=(0, 10))
    
    entry_girdi = tk.Entry(input_frame, width=50)
    entry_girdi.pack(side=tk.LEFT, padx=(0, 5))

    btn_gonder = tk.Button(input_frame, text="Yanıt Gönder ", command=Server.send_server_response, state=tk.DISABLED)
    btn_gonder.pack(side=tk.LEFT)

    root.bind('<Return>', lambda event: Server.send_server_response())
    
    #TKİNTER ARAYÜZİNDEKİ WIDGETLARI SERVER TARAFINDA KULLANMAK İÇİN
    Server.mesaj_alani = mesaj_alani
    Server.entry_girdi = entry_girdi
    Server.btn_start = btn_start
    Server.btn_stop = btn_stop
    Server.btn_gonder = btn_gonder
    Server.root = root
    
    root.mainloop()
    
    