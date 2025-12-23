import os
import sys
# RSA_Chiper.py'nin bulunduğu klasörü ekle
sys.path.append(os.path.abspath('client'))

from ECC_Chiper import SecureECC
from RSA_Chiper import SecureRSA

# Doğrudan proje içindeki klasörleri hedefle

SecureECC.generate_and_save_keys("server", "client")

print("Anahtarlar projenin içindeki server/ ve client/ klasörlerine kaydedildi.")