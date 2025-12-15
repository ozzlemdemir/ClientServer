import base64

class SimpleAESCipher:
  
    def __init__(self, key):
        self.ROUNDS = 16
        self.BLOCK_SIZE = 64 
        self.BYTE_SIZE = 8  
        
   
        master_key_bin = self._string_to_bin(key, self.BLOCK_SIZE)
        self.subkeys = self._generate_subkeys(master_key_bin)


    def _string_to_bin(self, text, length):
        
        byte_data = text.encode('utf-8')
        bin_string = ''.join(f'{byte:08b}' for byte in byte_data)
        
       
        if len(bin_string) < length:
             bin_string += '0' * (length - len(bin_string))
        elif len(bin_string) > length:
             bin_string = bin_string[:length]
             
        return bin_string

    def _xor_data(self, data1, data2):
      
        return ''.join(['1' if a != b else '0' for a, b in zip(data1, data2)])

    def _left_shift(self, data, count):
      
        count = count % len(data)
        return data[count:] + data[:count]

    def _pad_data(self, data_bytes):
    
        padding_needed = self.BYTE_SIZE - (len(data_bytes) % self.BYTE_SIZE)
        if padding_needed == 0:
             padding_needed = self.BYTE_SIZE
        return data_bytes + bytes([padding_needed] * padding_needed)

    def _unpad_data(self, data_bytes):
  
        if not data_bytes: return b""
        
        padding_len = data_bytes[-1]
        
        
        if 1 <= padding_len <= self.BYTE_SIZE:

            if all(data_bytes[i] == padding_len for i in range(len(data_bytes) - padding_len, len(data_bytes))):
                 return data_bytes[:-padding_len]
   
        return data_bytes 

    def _generate_subkeys(self, master_key_64bit):
        
        subkeys = []
        current_key = master_key_64bit
        for i in range(self.ROUNDS):
            shift_amount = (i % 3) + 1
            current_key = self._left_shift(current_key, shift_amount)
           
            subkeys.append(current_key[16:48]) 
        return subkeys 

    def _feistel_function(self, right_half_32bit, subkey_32bit):
       
        xor_result = self._xor_data(right_half_32bit, subkey_32bit)
        mixed_result = self._left_shift(xor_result, 4)
        return mixed_result

    def _process_block(self, block_64bit, subkeys, is_decrypt):
       
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

    def encrypt(self, text):
       
        plaintext_bytes = text.encode('utf-8')
        padded_bytes = self._pad_data(plaintext_bytes)
        
        ciphertext_bin_output = ""
        for i in range(0, len(padded_bytes), self.BYTE_SIZE):
            block_bytes = padded_bytes[i:i + self.BYTE_SIZE]
          
            block_bin = ''.join(f'{b:08b}' for b in block_bytes)
        
            cipher_block_bin = self._process_block(block_bin, self.subkeys, is_decrypt=False)
            ciphertext_bin_output += cipher_block_bin
     
        raw_bytes = bytes(int(ciphertext_bin_output[i:i+8], 2) for i in range(0, len(ciphertext_bin_output), 8))
        return base64.b64encode(raw_bytes).decode('utf-8')

    def decrypt(self, ciphertext_base64):
       
        try:
            raw_bytes = base64.b64decode(ciphertext_base64)
        except Exception:
            return "Base64 Çözme Hatası"
      
        ciphertext_bin = ''.join(f'{b:08b}' for b in raw_bytes)
        
        decrypted_bin_output = ""
        
        for i in range(0, len(ciphertext_bin), self.BLOCK_SIZE):
            block_bin = ciphertext_bin[i:i + self.BLOCK_SIZE]
            decrypted_block_bin = self._process_block(block_bin, self.subkeys, is_decrypt=True)
            decrypted_bin_output += decrypted_block_bin

        decrypted_raw_bytes = bytes(int(decrypted_bin_output[i:i+8], 2) for i in range(0, len(decrypted_bin_output), 8))

        unpadded_bytes = self._unpad_data(decrypted_raw_bytes)
        
        try:
        
            return unpadded_bytes.decode('utf-8').strip('\x00\r\n') 
        except UnicodeDecodeError:
            return f"Deşifreleme Hatası: {unpadded_bytes.hex()}"