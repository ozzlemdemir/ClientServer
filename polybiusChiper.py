class PolybiusChiper:
    def polybiusCipher(self, s):
        result = ""

        for char in s.lower():
            if not char.isalpha():
                continue 
            row = int((ord(char) - ord('a')) / 5) + 1
            col = ((ord(char) - ord('a')) % 5) + 1

            if char == 'k':
                row = row - 1
                col = 5 - col + 1
            elif ord(char) >= ord('j'):
                if col == 1:
                    col = 6
                    row = row - 1
                col = col - 1

            result += f"{row}{col}"

        return result
    def polybiusDeCipher(self, code):
        code = code.replace(" ", "")
        plaintext = ""
        for i in range(0, len(code), 2):
            pair = code[i:i+2]

            if len(pair) < 2 or not pair.isdigit():
                continue

            row = int(pair[0])
            col = int(pair[1])

            index = (row - 1) * 5 + (col - 1)
            char_code = ord('a') + index

            if char_code >= ord('j'):
                char_code += 1 

            char = chr(char_code)

            plaintext += char

        return plaintext
