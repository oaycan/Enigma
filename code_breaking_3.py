# Part 2 / Code breaking for Code-3
from enigma import *
import itertools as it

# crib word and the code to break
crib = "THOUSANDS"
code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"


# function for code breaking
def encryption(my_crib, my_code):
    # define all rotors, reflectors and ring setting options
    all_reflectors = ("A", "B", "C")
    all_rotors = ["II", "IV", "Beta", "Gamma"]
    ring_list = ["02", "04", "06", "08", "20", "22", "24", "26"]

    # create all 3-rotor options
    all_rotor_options = list(it.permutations(all_rotors, 3))

    # nested loop to iterate over all reflector, rotor and ring setting options
    for reflector in all_reflectors:
        for rotor_options in all_rotor_options:
            rotor1 = rotor_options[0]
            rotor2 = rotor_options[1]
            rotor3 = rotor_options[2]

            for ring_1 in ring_list:
                for ring_2 in ring_list:
                    for ring_3 in ring_list:

                        # create a ring setting option to check
                        rings = ring_1 + " " + ring_2 + " " + ring_3

                        # create an enigma machine with one of the rotor options and ring settings
                        my_enigma1 = Enigma(reflector + " " + rotor1 + " " + rotor2 + " " + rotor3)
                        my_enigma1.set_ring_settings(rings)
                        my_enigma1.set_rotor_initials("E M Y")
                        my_enigma1.set_plugboard_mappings("FH TS BE UQ KD AL")

                        # create a possible encryption
                        possible_encryption = my_enigma1.encode(my_code)

                        # check if the crib word is in the encrypted string
                        # and if so return the string content with the decoded message,
                        # reflector type, rotors and ring settings
                        if my_crib in possible_encryption:
                            string = f"Decoded Message: {possible_encryption} \nReflector: {reflector} " \
                                     f"\nRotors: {rotor1} {rotor2} {rotor3} \nRing Settings: {rings}"
                            return string


print(encryption(crib, code))