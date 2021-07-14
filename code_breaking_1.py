# Part 2 / Code breaking for Code-1
from enigma import *

# crib word and the code to break
crib = "SECRETS"
code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"


# function for code breaking
def encryption(my_crib, my_code):
    # reflector options
    all_reflectors = ("A", "B", "C")

    # check each reflector in a loop
    for reflector in all_reflectors:

        # enigma machine setup
        my_enigma1 = Enigma(reflector + " " + "Beta Gamma V")
        my_enigma1.set_rotor_initials("M J M")
        my_enigma1.set_ring_settings("04 02 14")
        my_enigma1.set_plugboard_mappings("KI XN FL")

        # create a possible encryption
        possible_encryption = my_enigma1.encode(my_code)

        # check if the crib word is in the encrypted string
        # and if so return the string content with the decoded message and the reflector type
        if my_crib in possible_encryption:
            string = f"Decoded Message: {possible_encryption} \nReflector: {reflector}"
            return string


print(encryption(crib, code))
