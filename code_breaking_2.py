# Part 2 / Code breaking for Code-2
from enigma import *

# crib word and the code to break
crib = "UNIVERSITY"
code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"


# function for code breaking
def encryption(my_crib, my_code):
    # Three nested loops for creating rotors' initial combinations
    for first_initial in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for second_initial in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for third_initial in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                initials = first_initial + " " + second_initial + " " + third_initial

                # setup enigma machine
                my_enigma1 = Enigma("B Beta I III")
                my_enigma1.set_ring_settings("23 02 10")
                my_enigma1.set_rotor_initials(initials)
                my_enigma1.set_plugboard_mappings("VH PT ZG BJ EY FS")

                # create a possible encryption
                possible_encryption = my_enigma1.encode(my_code)

                # check if the crib word is in the encrypted string
                # and if so return the string content with the decoded message and the starting position
                if my_crib in possible_encryption:
                    string = f"Decoded Message: {possible_encryption} \nStarting Position: {initials}"
                    return string


print(encryption(crib, code))
