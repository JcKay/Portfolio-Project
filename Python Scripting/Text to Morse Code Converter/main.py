MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '

        else:
            cipher += ' '

    return cipher


def decrypt(message):
    message += ' '
    decipher = ''
    halftext = ''
    space = 0
    for letter in message:
        # check of space
        if letter != ' ':
            space = 0
            halftext += letter

        else:
            # NOTE: in each alphabet in morse contain space. if we space message. there're two space.
            space += 1
            if space == 2:
                decipher += " "
            else:
                ## dict.values() to list and find index, find keys of values
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(halftext)]
                ## back to blank text, if one word finish
                halftext = ''

    return decipher


def main():
    methods = input('Choose method [encrypt for decrypt]: ')
    message = input("Type your messages: ").upper()

    if methods == "encrypt".lower() or methods == 'e':
        print(encrypt(message))
    elif methods == 'decrypt'.lower() or methods == 'd':
        print(decrypt(message))



if __name__ == '__main__':
    PROCESS = True
    while PROCESS:
        main()
        ask = input("press any key to continue\nexit: for exit\n")
        if ask == 'exit':
            PROCESS = False


