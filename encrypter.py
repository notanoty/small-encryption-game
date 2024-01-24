import pprint
import random


def textEncryption(text, encryptionDictionary):
    listText = list(text.lower())
    for i in range(len(listText)):
        listText[i] = encryptionDictionary.get(listText[i], listText[i])  # .get() will return the character itself if not found in dictionary
    return ''.join(listText)

def encrypt(text):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    encryptShufful = alphabet.copy()
    random.shuffle(encryptShufful)
    encryptionDictionary = {}
    for  i in range(0, len(alphabet)):
        encryptionDictionary[alphabet[i]] = encryptShufful[i]
    pprint.pprint(encryptionDictionary)
    return textEncryption(text, encryptionDictionary)

text = "In a quaint village nestled among rolling hills, a small bakery known for its delectable pastries stood as a beacon of warmth and tradition. Each morning, the air was filled with the aroma of freshly baked bread and cinnamon, drawing locals and travelers alike. Inside, the walls adorned with family pictures told stories of generations of bakers. The bakery, more than just a place for food, was a testament to the community's spirit and history."

# pprint.pprint(text.split())

pprint.pprint(encrypt(text))

