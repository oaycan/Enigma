# Part 2 / Code breaking for Code-4
from enigma import *

# crib and code to break
crib = "TUTOR"
code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"


# function for code breaking
def encryption(crib, code):
    # Plugs left empty on the plugboard
    plugs_empty = "DEKLMOQTUXYZ"

    # output initialization
    output = ""

    # loop for iterating the unknown character on the first pair
    for char1 in plugs_empty:
        # create the first pair option to check
        first = "A" + char1

        # new string excluding the checked character above
        new_plugs_empty = plugs_empty.replace(char1, "")

        # loop for iterating the unknown letter on the second pair over the new string new_plugs_empty
        for char2 in new_plugs_empty:
            # create the second pair option to check
            second = "I" + char2

            # enigma machine setup
            my_enigma1 = Enigma("A V III IV")
            my_enigma1.set_ring_settings("24 12 10")
            my_enigma1.set_rotor_initials("S W U")
            my_enigma1.set_plugboard_mappings("WP RJ " + first + " VF " + second + " HN CG BS")

            # create a possible encryption
            possible_encryption = my_enigma1.encode(code)

            # check if the crib word is in the encrypted string
            # and if so return the string content with the decoded message, reflector type and
            # the possible plugboard pairs and finally add them to the output string
            if crib in possible_encryption:
                plugboard_string = "WP RJ " + first + " VF " + second + " HN CG BS"
                string = f"Decoded Message: {possible_encryption} \nPlugboard Pairs: {plugboard_string}\n"
                output += string + "\n"

    return output

print(encryption(crib, code))
