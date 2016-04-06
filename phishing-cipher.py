#!/usr/bin/env python

def encodeMessage(message, offset):
    plainMessage = ''

    for char in message:
        if char.isalpha():
            num = ord(char)
            num += int(offset)
            if char.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif char.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            plainMessage += chr(num)
        else:
            plainMessage += char

    return plainMessage


print("Character Offset: ")
offset = raw_input()

print("Enter message to decode: ")
cipherMessage = raw_input()

print encodeMessage(cipherMessage, offset)[::-1]

