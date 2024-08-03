import curses
# import pprint
import random
from colorama import Fore, Back, Style
import shutil

def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def text_encryption(text, encryption_dictionary):
    list_text = list(text.lower())
    for i in range(len(list_text)):
        list_text[i] = encryption_dictionary.get(list_text[i], list_text[i])  
    return ''.join(list_text)



def encrypt(text):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    encrypt_shufful = alphabet.copy()
    random.shuffle(encrypt_shufful)
    encryption_dictionary = {}
    for  i in range(0, len(alphabet)):
        encryption_dictionary[alphabet[i]] = encrypt_shufful[i]
    return text_encryption(text, encryption_dictionary)


def count_cherecters(text):
    char_count = {}  # Dictionary to store the count of each character
    for char in text:
        if char in [' ', ',', '.', "'"]:
            continue
        if char in char_count:
            char_count[char] += 1  # Increment count if character is already in the dictionary
        else:
            char_count[char] = 1  # Initialize count for new characters
    char_count = sorted(char_count.items(), key=lambda x:x[1])  
    return char_count

def print_encrypted_text(win, encrypted_text , decryption_dictionary: dict):
    list_text = list(encrypted_text.lower())
    max_line_size = 100
    current_line_x = 1
    current_line_y = 0
    for i in range(len(list_text)):
        
        if list_text[i] == " " and current_line_x > max_line_size:
            # print()
            current_line_x = 0
            current_line_y += 1
        elif list_text[i] in ['.', ',', "'"]:
            win.addstr(current_line_y, current_line_x, list_text[i])
            # print(list_text[i], end="")
        elif list_text[i] in decryption_dictionary.keys():
            win.addstr(current_line_y, current_line_x, decryption_dictionary[list_text[i]] , curses.color_pair(curses.COLOR_GREEN) )
            # print(Fore.GREEN + decryption_dictionary[list_text[i]] + Fore.RESET, end="" )
        else:
            win.addstr(current_line_y, current_line_x, list_text[i], curses.color_pair(curses.COLOR_YELLOW))
            # print(Fore.YELLOW + list_text[i] + Fore.RESET, end="")
        current_line_x += 1
        
    print()
    pass



def decryption_game(text):
    decryption_dictionary = {}
    game = True

    win = curses.initscr()
    curses.noecho()
    curses.start_color()    
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i , i, 0)

    while(game):
        decrypted_text = text_encryption(text, decryption_dictionary)
        # pprint.pprint(count_cherecters(decrypted_text))
        print_encrypted_text(win, text, decryption_dictionary)
        player_input = chr(win.getch())
        if(player_input in ['R', 'r']):
            y, x = win.getmaxyx()
            win.addstr(y - 2, 0, "Replace ")
            win.move(y - 2, 8) 
            current_letter = chr(win.getch())
            win.addch(y - 2, 8, current_letter)

            win.addstr(y - 2, 10, "with")
            win.move(y - 2, 15) 
            replce_letter = chr(win.getch())
            win.addch(y - 2, 15, replce_letter) 
            if current_letter not in decryption_dictionary:
                decryption_dictionary[current_letter] = replce_letter
            win.clear()
        elif(player_input in ['q', 'Q']):        
            break  

        win.move(0, 0) 

def main():
    text = "In a quaint village nestled among rolling hills, a small bakery known for its delectable pastries stood as a beacon of warmth and tradition. Each morning, the air was filled with the aroma of freshly baked bread and cinnamon, drawing locals and travelers alike. Inside, the walls adorned with family pictures told stories of generations of bakers. The bakery, more than just a place for food, was a testament to the community's spirit and history."
    text = encrypt(text)
    decryption_game(text)

