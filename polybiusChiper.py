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
