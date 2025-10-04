

encrypted_message = '' #şifrelenmiş mesajı tutar
decrypted_message = '' #şifresi çözülmüş mesajı tutar

alphabet=['a','b' ,'c' , 'd', 'e', 'f', 'g' ,'h' ,'i' ,'j','k' ,'l' ,'m' ,'n' ,
    'o' ,'p' ,'r' ,'s' ,'t' ,'u' ,'v', 'y' ,'z']  



def sezar_sifrele(decrypted_message):
    sifreli_mesaj = ''
    for i in decrypted_message:
     sifreli_mesaj += alphabet[(alphabet.index(i)+3) % len(alphabet)]
    return sifreli_mesaj
print("The encrypted message is:", encrypted_message)

def sezar_coz(encrypted_message):
    sifresiz_mesaj = ''
    for i in encrypted_message:
     sifresiz_mesaj += alphabet[(alphabet.index(i)-3) % len(alphabet)]
    return sifresiz_mesaj
print("The decrypted message is:", decrypted_message)