# Part 2 / Code breaking for Code-4
from enigma import *
import itertools as it

cribs = ["FACEBOOK", "WHATSAPP", "YOUTUBE", "TIKTOK", "INSTAGRAM", "SNAPCHAT", "TWITTER", "PINTEREST", "LINKEDIN", "VIBER", "DISCORD"]
code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"


# function for code breaking
def encryption(my_cribs, my_code):
    # reflector options
    all_reflectors = ("A", "B", "C")

    # create all possible pair of letters that can be modified
    for reflector in all_reflectors:
        pairs = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        my_enigma1 = Enigma(reflector + " V II IV")
        my_enigma1.set_ring_settings("06 18 07")
        my_enigma1.set_rotor_initials("A J L")
        my_enigma1.set_plugboard_mappings("UG IE PO NX WT")

        # modify the reflector mappings according to selected pairs of letters
        while len(alphabet) != 0:
            char1 = alphabet[0]
            char2 = my_enigma1.re_list[0].rotor_mappings[reflector][0]

            # create a pair of letters and add it to the list of pairs
            one_pair = char1 + char2
            pairs.append(one_pair)

            # exclude the selected pairs from the alphabet list
            alphabet = alphabet.replace(char1, "")
            alphabet = alphabet.replace(char2, "")

            # modify the reflector mappings accordingly
            my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(char1, "")
            my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(char2, "")

        # create full combinations of four pairs of letters
        # as sender did by taking two wires and repeated the process two times
        all_pairs = list(it.combinations(pairs, 4))

        # try all options for four pairs of letters and search crib word in code
        for four_pairs in all_pairs:
            # there are 3 options that four pairs of letters can be created
            possibilities = ([(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)])

            # create all enigma machines using the possibilities
            for comb in possibilities:
                my_enigma1 = Enigma(reflector + " V II IV")
                my_enigma1.set_ring_settings("06 18 07")
                my_enigma1.set_rotor_initials("A J L")
                my_enigma1.set_plugboard_mappings("UG IE PO NX WT")
                modifications = ""

                # create modified pair options
                for my_pair in comb:
                    x, y = my_pair
                    a = four_pairs[x][0]
                    b = four_pairs[x][1]
                    c = four_pairs[y][0]
                    d = four_pairs[y][1]

                    # apply the modifications to the reflector mappings
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(b, "0")
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(d, b)
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace("0", d)
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(a, "1")
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace(c, a)
                    my_enigma1.re_list[0].rotor_mappings[reflector] = my_enigma1.re_list[0].rotor_mappings[reflector].replace("1", c)

                    # create an option for the modification
                    modifications += a + d + " " + c + b + " "

                # create a possible encryption
                possible_encryption = my_enigma1.encode(my_code)

                # check if the crib word is in the encrypted string and if so return the string content with
                # the decoded message, reflector type and the full plugboard status with the modifications
                for crib in my_cribs:
                    if crib in possible_encryption:
                        modifications = modifications[:-1]
                        string = f"Decoded Message: {possible_encryption} \nReflector: {reflector} \nModifications: {modifications}"
                        return string

print(encryption(cribs, code))