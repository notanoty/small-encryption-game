import curses
# import pprint
import random
from colorama import Fore, Back, Style
import shutil

def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def text_decryption(text, encryption_dictionary):
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
    return text_decryption(text, encryption_dictionary)


def count_letters(text):
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
            current_line_x = 0
            current_line_y += 1
        elif list_text[i] in ['.', ',', "'"]:
            win.addstr(current_line_y, current_line_x, list_text[i])
        elif list_text[i] in decryption_dictionary.keys():
            win.addstr(current_line_y, current_line_x, decryption_dictionary[list_text[i]] , curses.color_pair(curses.COLOR_GREEN) )
        else:
            win.addstr(current_line_y, current_line_x, list_text[i], curses.color_pair(curses.COLOR_YELLOW))
        current_line_x += 1
        
    print()
    pass


def encrypted_text_len(encrypted_text):
    list_text = list(encrypted_text.lower())
    max_line_size = 100
    current_line_x = 1
    current_line_y = 0
    max_x = 0
    for i in range(len(list_text)):
        if list_text[i] == " " and current_line_x > max_line_size:
            if max_x < current_line_x:
                max_x = current_line_x
            current_line_x = 0
            current_line_y += 1
        current_line_x += 1
    return (current_line_y, max_x)


def command_line(win, list_text: list, inputs_amount: int):
    y, _ = win.getmaxyx()
    x_poasition = 0
    inputs = []
    for i in range(inputs_amount):
        if i < len(list_text):
            element = list_text[i]
            win.addstr(y - 1, x_poasition, element)
            x_poasition += len(element) + 1
        win.move(y - 1, x_poasition)
        current_letter = chr(win.getch())
        win.addch(y - 1, x_poasition, current_letter)
        x_poasition += 2
        inputs.append(current_letter)
    return inputs

def analyze_letter(letter_info, decrypt_dictionary):
    for letter in decrypt_dictionary.keys():
        if letter_info[0] == letter:
            return (decrypt_dictionary[letter], True)
    return (letter_info[0], False)


def decrypt_dictionary(letters_info, decrypt_dictionary):
    decrepted_dictionary = {}
    for letter_info in letters_info:
        letter, is_decrypted = analyze_letter(letter_info, decrypt_dictionary)
        if is_decrypted:
            leter_description = f"1{letter}"
            decrepted_dictionary[leter_description] = letter_info[1]
        else:
            leter_description = f"0{letter}"
            decrepted_dictionary[leter_description] = letter_info[1]
    return decrepted_dictionary

def show_interface(win, text, decryption_dictionary):
        text_y_len, _ = encrypted_text_len(text)
        print_encrypted_text(win, text, decryption_dictionary)
        letters_info =  count_letters(text)
        letters_info_decrypted = decrypt_dictionary(letters_info, decryption_dictionary)

        win.addstr(text_y_len + 1, 0, "Letter Frequency")
        letter_info_position = text_y_len + 2
        
        for letter_info in letters_info_decrypted.items():
            if letter_info[0][0] == "1":
                win.addstr(letter_info_position, 0, f"{letter_info[0][1]} : {letter_info[1]}", curses.color_pair(curses.COLOR_GREEN) )
            else:
                win.addstr(letter_info_position, 0, f"{letter_info[0][1]} : {letter_info[1]}" )
            letter_info_position += 1

        win.addstr(text_y_len + 1, 20, "Decryption Dictionary")
        decryption_dictionary_position = text_y_len + 2
        for letter_info in decryption_dictionary.items():
            win.addstr(decryption_dictionary_position, 20, f"{letter_info[0]} : {letter_info[1]}", curses.color_pair(curses.COLOR_GREEN))
            decryption_dictionary_position += 1


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
        # decrypted_text = text_decryption(text, decryption_dictionary)
        # print(decryption_dictionary) 
        show_interface(win, text, decryption_dictionary)


        player_input = chr(win.getch())
        if(player_input in ['R', 'r']):
            current_letter, replace_letter = command_line(win, ["Replace", "with"], 2 )
            
            if current_letter not in decryption_dictionary:
                decryption_dictionary[current_letter] = replace_letter
            win.clear()
        elif(player_input in ['q', 'Q']):        
            break  

        win.move(0, 0) 

def main():
    text = "In a quaint village nestled among rolling hills, a small bakery known for its delectable pastries stood as a beacon of warmth and tradition. Each morning, the air was filled with the aroma of freshly baked bread and cinnamon, drawing locals and travelers alike. Inside, the walls adorned with family pictures told stories of generations of bakers. The bakery, more than just a place for food, was a testament to the community's spirit and history."
    text = encrypt(text)
    decryption_game(text)

