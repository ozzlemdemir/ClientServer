import base64

class DESCipher:

    def __init__(self):
        self.ROUNDS = 16
        self.BLOCK_SIZE = 64 
        self.BYTE_SIZE = 8   
    

    def _xor_data(self, data1, data2):
      
        return ''.join(['1' if a != b else '0' for a, b in zip(data1, data2)])

    def _left_shift(self, data, count):
       
        count = count % len(data)
        return data[count:] + data[:count]
        
    def _string_to_bin(self, text, length):
        
        byte_data = text.encode('utf-8')
        bin_string = ''.join(f'{byte:08b}' for byte in byte_data)
        
       
        if len(bin_string) < length:
            
            padding_len = length - len(bin_string)
            bin_string += '1' 
            bin_string += '0' * (padding_len - 1)
       

        return bin_string

    def _generate_subkeys(self, master_key_64bit):
        """Master Key'den 16 adet alt anahtar üretir."""
        subkeys = []
        current_key = master_key_64bit
        for i in range(self.ROUNDS):
            shift_amount = (i % 3) + 1
            current_key = self._left_shift(current_key, shift_amount)
           
            subkey = current_key[16:48] 
            subkeys.append(subkey)
        return subkeys

    def _feistel_function(self, right_half_32bit, subkey_32bit):
        """Basitleştirilmiş Feistel Fonksiyonu F(R, K)."""
        xor_result = self._xor_data(right_half_32bit, subkey_32bit)
        mixed_result = self._left_shift(xor_result, 4)
        return mixed_result

    def _process_block(self, block_64bit, subkeys, is_decrypt):
        """Tek bir 64-bit bloğu şifreler/deşifreler."""
        if is_decrypt:
            subkeys = subkeys[::-1]
            
        L = block_64bit[:32]
        R = block_64bit[32:]
        
        for i in range(self.ROUNDS):
            L_prev = L
            L = R
            F_result = self._feistel_function(R, subkeys[i])
            R = self._xor_data(L_prev, F_result)

        return R + L 


    def encrypt(self, text, key):
       
        master_key_bin = self._string_to_bin(key, self.BLOCK_SIZE)
        subkeys = self._generate_subkeys(master_key_bin)
   
        text_bytes = text.encode('utf-8')
  
        padding_needed = self.BYTE_SIZE - (len(text_bytes) % self.BYTE_SIZE)
        if padding_needed == self.BYTE_SIZE:
            padding_needed = 0

        padded_bytes = text_bytes + bytes([padding_needed] * padding_needed)

        cipher_bin_output = ""
        for i in range(0, len(padded_bytes), self.BYTE_SIZE):
            block_bytes = padded_bytes[i:i + self.BYTE_SIZE]

            block_bin = ''.join(f'{b:08b}' for b in block_bytes)

            cipher_block_bin = self._process_block(block_bin, subkeys, is_decrypt=False)
            cipher_bin_output += cipher_block_bin

        raw_bytes = bytes(int(cipher_bin_output[i:i+8], 2) for i in range(0, len(cipher_bin_output), 8))
        base64_encoded = base64.b64encode(raw_bytes).decode('utf-8')
        
        return base64_encoded

    def decrypt(self, ciphertext_base64, key):

        master_key_bin = self._string_to_bin(key, self.BLOCK_SIZE)
        subkeys = self._generate_subkeys(master_key_bin)

        try:
            raw_bytes = base64.b64decode(ciphertext_base64)
            ciphertext_bin = ''.join(f'{b:08b}' for b in raw_bytes)
        except Exception:
            return "Base64 Çözme Hatası"
        
        decrypted_bin_output = ""
        for i in range(0, len(ciphertext_bin), self.BLOCK_SIZE):
            block_bin = ciphertext_bin[i:i + self.BLOCK_SIZE]

            decrypted_block_bin = self._process_block(block_bin, subkeys, is_decrypt=True)
            decrypted_bin_output += decrypted_block_bin

        decrypted_raw_bytes = bytes(int(decrypted_bin_output[i:i+8], 2) for i in range(0, len(decrypted_bin_output), 8))


        if not decrypted_raw_bytes:
            return ""
            
        padding_len = decrypted_raw_bytes[-1]

        if 0 < padding_len <= self.BYTE_SIZE:
           
            final_bytes = decrypted_raw_bytes[:-padding_len]
        else:
            
            final_bytes = decrypted_raw_bytes

        try:
            return final_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return "Çözülen metin okunamıyor (Unicode Hatası)"