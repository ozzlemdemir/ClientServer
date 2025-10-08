import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import sys
#from sezar import sezar_coz



#HOST = input("Sunucu IP adresini girin (varsayılan : ") #varsayılan adres :"127.0.0.1"
# PORT_INPUT = input("Sunucu port numarasını girin (varsayılan 12345): ")
#PORT=int(PORT_INPUT)
#HOST="127.0.0.1"
#PORT=12345
host_input = input("Sunucu IP adresini girin (varsayılan: 127.0.0.1): ")
HOST = host_input if host_input else "127.0.0.1"

port_input = input("Sunucu port numarasını girin (varsayılan: 12345): ")
PORT = 0 # PORT'u başlangıçta tanımla
conn=None

if not port_input:
    # Kullanıcı boş bıraktıysa varsayılan portu kullan
    PORT = 12345
else:
    try:
        # Tırnak işaretlerini (", ') ve boşlukları temizleyerek int'e çevir
        temiz_port = port_input.strip().strip('"').strip("'")
        PORT = int(temiz_port)
        
        # Portun geçerli bir aralıkta olup olmadığını kontrol et
        if not (1024 <= PORT <= 65535):
            print("UYARI: Port numarası 1024 ile 65535 arasında olmalıdır. Varsayılan (12345) kullanılıyor.")
            PORT = 12345
            
    except ValueError:
        print(f"geçersiz port numarası")
        PORT = 12345

print(f"\nSunucu Başlatılıyor: IP={HOST}, PORT={PORT}")

SERVER_RUNNING = False
#client_connections = [] # Aktif istemci bağlantılarını (socket objelerini) tutacak liste

def start_server():
    """Sunucu soketini başlatır ve istemci bağlantılarını dinlemeyi başlatır."""
    global server_socket, SERVER_RUNNING

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        SERVER_RUNNING = True
        mesaj_ekle("SUNUCU", f"Server dinlemede: {HOST}:{PORT}")

        # Arayüzü güncelle
        btn_start.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)
        btn_gonder.config(state=tk.NORMAL) # Mesaj gönderme butonunu aktifleştir

        # Dinleme işlemini ayrı bir thread'de başlat
        threading.Thread(target=accept_connections, daemon=True).start()

    except socket.error as e:
        SERVER_RUNNING = False
        mesaj_ekle("HATA", f"Sunucu başlatılamadı. Hata: {e}")
        btn_start.config(state=tk.NORMAL)
        btn_gonder.config(state=tk.DISABLED)

def accept_connections():
    """Gelen istemci bağlantısını kabul eder."""
    while SERVER_RUNNING:
        global conn 
        try:
            conn, addr = server_socket.accept()
            mesaj_ekle("BAĞLANTI", f"Client bağlandı: {addr}")
             
            conn = conn 
            # Client'a ilk mesajı gönder
            conn.send("Bağlantı başarılı. Mesajınızı yazabilirsiniz.".encode("utf-8"))
            
            # Her client için ayrı bir dinleme thread'i başlat
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            
        except socket.error as e:
            if SERVER_RUNNING:
                mesaj_ekle("HATA", f"Bağlantı kabul hatası: {e}")

def handle_client(conn, addr):
    """Belirli bir istemciden gelen mesajları dinler."""
    while True: #sürekli dinle
        try:
            data = conn.recv(1024)
            if not data:
                mesaj_ekle("BAĞLANTI", f"Client bağlantıyı kesti: {addr}")
                break

            #mesaj = sezar_coz(data.decode("utf-8"))
            mesaj=data.decode("utf-8")
            mesaj_ekle("CLIENT", f"({addr[1]}): {mesaj}")

            if mesaj.lower() == "exit":
                mesaj_ekle("BAĞLANTI", f"Client çıkış yaptı: {addr}")
                conn.send("Görüşmek üzere!".encode("utf-8"))
                break

            

        except socket.error as e:
            mesaj_ekle("HATA", f"Client ({addr[1]}) ile iletişim hatası: {e}")
            break
    conn.close()

def stop_server():
    """Çalışan sunucuyu güvenli bir şekilde kapatır."""
    global SERVER_RUNNING

    if not SERVER_RUNNING:
        mesaj_ekle("UYARI", "Sunucu zaten durdu.")
        return
    else:
     SERVER_RUNNING = False
            
    try:
       
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((HOST, PORT))
        server_socket.close()
        mesaj_ekle("SUNUCU", "Sunucu durduruldu.")
    except Exception as e:
        mesaj_ekle("HATA", f"Sunucuyu durdurma hatası: {e}")

    # Arayüzü güncelle
    btn_start.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)
    btn_gonder.config(state=tk.DISABLED)


def send_server_response():
    """Sunucudan istemciye mesaj gönderir."""
    global conn
    mesaj = entry_girdi.get().strip()
    if not mesaj:
        return

    if not conn:
        mesaj_ekle("UYARI", "Henüz istemci bağlı değil.")
        return

    try:
        conn.send(mesaj.encode("utf-8"))
        mesaj_ekle("SERVER", f"(Client'a): {mesaj}")
        entry_girdi.delete(0, tk.END)
    except socket.error as e:
        mesaj_ekle("HATA", f"Mesaj gönderilemedi: {e}")

# --- 2. Arayüz Fonksiyonları (Utility) ---

def mesaj_ekle(kaynak, metin):
    """Gelen/Giden mesajları ana mesaj alanına ekler."""
    mesaj_alani.config(state=tk.NORMAL)
    mesaj_alani.insert(tk.END, f"[{kaynak}]: {metin}\n")
    mesaj_alani.yview(tk.END)
    mesaj_alani.config(state=tk.DISABLED)

def on_closing():
    """Pencere kapatıldığında sunucuyu durdurur ve uygulamayı kapatır."""
    stop_server()
    root.destroy()


# --- 3. Arayüz Tasarımı (Ana Pencere) ---

root = tk.Tk()
root.title("Python Chat Server")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Mesaj Alanı
mesaj_alani = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=60)
mesaj_alani.pack(padx=10, pady=10)

# Butonlar için Frame
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=(0, 10))

# Başlat Butonu
btn_start = tk.Button(button_frame, text="SERVER'I BAŞLAT", command=start_server, fg="green")
btn_start.pack(side=tk.LEFT, padx=5)

# Durdur Butonu
btn_stop = tk.Button(button_frame, text="SERVER'I DURDUR", command=stop_server, fg="red", state=tk.DISABLED)
btn_stop.pack(side=tk.LEFT, padx=5)

# Mesaj gönderme alanı (Entry ve Button)
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10))

# Mesaj Giriş Kutusu
entry_girdi = tk.Entry(input_frame, width=50)
entry_girdi.pack(side=tk.LEFT, padx=(0, 5))

# Gönder Butonu (Başlangıçta pasif)
btn_gonder = tk.Button(input_frame, text="Yanıt Gönder (Tüm Client'lara)", command=send_server_response, state=tk.DISABLED)
btn_gonder.pack(side=tk.LEFT)

# Enter tuşuna basıldığında mesaj gönderme işlevi ekle
root.bind('<Return>', lambda event: send_server_response())


# --- 4. Uygulamayı Başlat ---

root.mainloop()