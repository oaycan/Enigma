# Super class of all other classes
class Enigma:
    def __init__(self, rotors_reflectors):

        # initialize rotor and reflector lists and assign my_plugboard as Plugboard class object
        self.ro_list = []
        self.re_list = []
        self.my_plugboard = Plugboard()

        # create a list with all rotors and reflectors using their input names and orders
        rot_ref_list = []
        char = ""
        for ltr in rotors_reflectors:
            if ltr != " ":
                char += ltr
            else:
                rot_ref_list.append(char)
                char = ""
        rot_ref_list.append(char)

        # create separate lists for rotors and reflectors keeping their input orders
        for item in rot_ref_list:
            if item in ["A", "B", "C", "B-Thin"]:
                self.re_list.append(RotorSection(item))
            else:
                self.ro_list.append(RotorSection(item))

    # instance method for encoding the input string
    def encode(self, string):
        # case sensitivity ignored for the string to be encoded
        string = string.upper()

        # initialize the output string which will be returned as a result of the encoded message
        encoded_string = ""

        # rotation function for the rotors
        def rotation(rot_list):
            rot_list[-number - 1].rotor_mappings[rot_list[-number - 1].rotor_type] = \
                rot_list[-number - 1].rotor_mappings[
                    rot_list[-number - 1].rotor_type][1:] + \
                rot_list[-number - 1].rotor_mappings[rot_list[-number - 1].rotor_type][0]

            rot_list[-number - 1].ring_positions[rot_list[-number - 1].rotor_type] = \
                rot_list[-number - 1].ring_positions[
                    rot_list[-number - 1].rotor_type][1:] + \
                rot_list[-number - 1].ring_positions[rot_list[-number - 1].rotor_type][0]

            rot_list[-number - 1].ring_main[rot_list[-number - 1].rotor_type] = \
                rot_list[-number - 1].ring_main[
                    rot_list[-number - 1].rotor_type][1:] + \
                rot_list[-number - 1].ring_main[rot_list[-number - 1].rotor_type][0]

        # Create rotor and reflector lists and index value for signal flow of the Enigma machine
        for character in string:

            # check if the string is correctly entered using the available keys on enigma, if not raise a ValueError
            if character in RotorSection.housing_contacts:
                character = self.my_plugboard.encode(character).upper()

                # create an index value which will be the main key element for signal flow through pins and contacts
                index = RotorSection.housing_contacts.index(character)
                rot_list = self.ro_list
                ref_list = self.re_list

            else:
                raise ValueError("Invalid letter entry! It should be within A to Z")

            for number in range(len(rot_list)):
                if (-number - 1) == -1:
                    notch = rot_list[-number - 1].notch_position[rot_list[-number - 1].rotor_type]
                    display = rot_list[-number - 1].ring_main[rot_list[-number - 1].rotor_type][0]
                    rotation(rot_list)

                    if display == notch:
                        rot_list[-number - 1].flag0 = True

                if (-number - 1) > -1:
                    display1 = rot_list[-number - 1].ring_main[rot_list[-number - 1].rotor_type][0]
                    notch = rot_list[-number - 1].notch_position[rot_list[-number - 1].rotor_type]

                    if rot_list[-number].flag0 or (display1 == notch and not((-number - 1) == -len(rot_list))):
                        rotation(rot_list)

                        rot_list[-number].flag0 = False
                        if display1 == notch:
                            rot_list[-number - 1].flag1 = True

                # encoding process using the signal flow through all rotors and reflectors in the Enigma machine
                # and we get the index value of the signal with respect to housing contacts/letters
            for rotors in list(reversed(rot_list)):
                index = rotors.encode_right_to_left(index)

            for reflectors in list(reversed(ref_list)):
                index = reflectors.encode_right_to_left(index)

            for rotors in rot_list:
                index = rotors.encode_left_to_right(index)

                # send the signal to plugboard for the final encoding process
            encoded_string += self.my_plugboard.encode(RotorSection.housing_contacts[index])

            # return the final encoded string
        return encoded_string

        # instance method for setting rotor initials

    def set_rotor_initials(self, new_initials):
        x = 0
        for index, rotors in enumerate(self.ro_list):
            rotors.rotor_initials(new_initials[index + x])
            x += 1

        # instance method for setting ring settings

    def set_ring_settings(self, new_rings):
        x = 2
        for index, rotors in enumerate(self.ro_list):
            rotors.ring_settings(new_rings[index + x - 2:index + x])
            x += 2

        # instance method for setting plugboard mappings

    def set_plugboard_mappings(self, mappings):
        lead_mappings = []
        char = ""

        # create the leads
        for ltr in mappings:
            if ltr != " ":
                char += ltr
            else:
                lead_mappings.append(char)
                char = ""
        lead_mappings.append(char)

# Class for Leads in Enigma Machine
class PlugLead:
    # Letters on Enigma keyboard as a class variable
    keyboard = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z", " ", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

    # Constructor function for the class PLugLead
    def __init__(self, mapping):
        # Accepts both lower & upper case letter mapping entries from the user
        mapping = mapping.upper()

        # Check if the mapping entry is a valid one / if string with length two and letters from Enigma keyboard
        # if not raise a ValueError
        if len(mapping) == 2 and (mapping[0] in PlugLead.keyboard and mapping[1] in PlugLead.keyboard) and mapping[0] != \
                mapping[1]:
            self.mapping = mapping
        else:
            raise ValueError("Invalid entry! Please enter 2 different letters only from Enigma keyboard.")

    # Instance Method which returns the encoded letter
    def encode(self, character):
        # not case sensitive for the entry
        character = character.upper()

        # Check if the argument/letter is a valid one / 1 letter length and from Enigma keyboard
        # If not return ValueError
        if len(character) == 1 and character in PlugLead.keyboard:

            # Check if argument/letter is in the instance variable mapping and return accordingly
            # if not return the character itself
            if character in self.mapping and self.mapping.index(character) == 1:
                return self.mapping[0]
            elif character in self.mapping and self.mapping.index(character) == 0:
                return self.mapping[1]
            else:
                return character

        else:
            raise ValueError("Invalid entry! Please enter 1 letter only from Enigma keyboard.")


# class for Plugboard in the Enigma machine
class Plugboard:
    # letters on Enigma keyboard as a class variable
    keyboard = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z", " ", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

    # constructor for Plugboard
    def __init__(self):
        # list for used plugs
        self.used_plugs = []
        self.mapping_string = ""

    # instance Method which lists the plugs (objects) occupied with leads in plugboard of the enigma machine
    def add(self, pluglead):

        # check if any of the plugs of the pluglead object already in use in the plugboard, if so raise a ValueError
        # if not add it to the used_plugs
        if pluglead.mapping[0] in self.mapping_string or pluglead.mapping[1] in self.mapping_string:
            raise ValueError("One or both of the plugs in the mapping entered is already in use on the plugboard!")
        else:
            # construct a list with all used pluglead objects
            self.used_plugs += [pluglead]

            # construct a string that contains all mappings of plugleads in the plugboard
            self.mapping_string += pluglead.mapping

    # Instance Method which searches the character(letter) in the list of filled plugs and returns the encoded letter
    def encode(self, character):
        # not case sensitive for the entry
        character = character.upper()

        # Check if the argument/letter is a valid one / 1 letter length and from Enigma keyboard
        # If not return ValueError
        if len(character) == 1 and character in Plugboard.keyboard:

            # Check if the argument/letter is available in any of the lead objects in list used_plugs
            # If so return the encoded letter accordingly, if not return the argument/letter itself
            for plug in self.used_plugs:
                if character in plug.mapping:
                    if plug.mapping.index(character) == 0:
                        return plug.mapping[1]
                    else:
                        return plug.mapping[0]

            return character
        else:
            raise ValueError("Invalid entry! Please enter 1 letter only from Enigma keyboard.")

    # Extra : Show the status of plugboard by listing all used plugs with leads
    def status(self):
        return [plug.mapping for plug in self.used_plugs]


# Class for rotor section of Enigma
class RotorSection:
    # String class variable represents the rotor housing contacts connected to the letters in plugboard
    housing_contacts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896"

    # Constructor for the class RotorSection
    def __init__(self, rotor_type):
        # Rotor default mappings for the initial rotor position AAA with respect to the housing contacts
        self.rotor_mappings = {
            "I":    "EKMFLGDQVZNTOWYHXUSPAIBRCJ0.213546 879", "II":     "AJDKSIRUXBLHWTMCQGZNPYFVOE987.5641320 ",
            "III":  "BDFHJLCPRTXVZNYEIWGAKMUSQO1352476.0 98", "IV":     "ESOVPZJAYQUIRHXLNFTGKDCMWB86754230. 19",
            "V":    "VZBRGITYUPSDNHLXAWMJQOFECK647.583291 0", "VI":     "JPGVOUMFYQBENHZRDKASXLICTW 68.79052431",
            "VII":  "NZJHGRCXMYSWBOUFAIVLPEKQDT93748. 51260", "VIII":   "FKQHTLXOCBJSPDZRAMEWNIUYGV273 64.15089",
            "A":    "EJMZALYXVBWFCRQUONTSPIKHGD837402961 5.", "B":      "YRUHQSLDPXNGOKMIEBFZCWVJAT12 08.745369",
            "C":    "FVPJIAOYEDRZXWGCTKUQSBNMHL0 65.9238741", "B-Thin": "ENKQAUYWJICOPBLMDXZVFTHRGS0 218796435.",
            "Beta": "LEYJVCNIXWPBQMDRTAKZGFUHOS8475906123 .", "Gamma":  "FSOKANUERHMBTIYCWLQPZXVGJD9475.86 1320"
        }

        self.ring_positions = {
            "I":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "II":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "III":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "IV":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "V":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "VI":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "VII":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "VIII":   "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "A":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "B":      "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "Beta": "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "B-Thin": "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "C":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "Gamma":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896"
        }

        self.ring_main = {
            "I":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "II":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "III":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "IV":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "V":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "VI":     "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "VII":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "VIII":   "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "A":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "B":      "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "Beta": "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "B-Thin": "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896",
            "C":    "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896", "Gamma":  "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345.7896"
        }

        # rotor notch positions
        self.notch_position = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z", "Beta": "", "Gamma": ""}
        # flags for enabling rotors to advance when needed
        self.flag0 = False
        self.flag1 = False

        # Check if the rotor_type entered is a valid one, if not raise a ValueError
        if rotor_type in self.rotor_mappings.keys():
            self.rotor_type = rotor_type
        else:
            raise ValueError("not a valid rotor name!")

    # instance method for changing ring settings
    def ring_settings(self, settings):
        self.rotor_mappings[self.rotor_type] = self.rotor_mappings[self.rotor_type][-(int(settings) - 1):] + \
                                               self.rotor_mappings[self.rotor_type][:-(int(settings) - 1)]

        self.ring_positions[self.rotor_type] = self.ring_positions[self.rotor_type][-(int(settings) - 1):] + \
                                               self.ring_positions[self.rotor_type][:-(int(settings) - 1)]

    # instance method for changing rotor initial values
    def rotor_initials(self, initial):
        index = RotorSection.housing_contacts.index(initial)
        self.rotor_mappings[self.rotor_type] = self.rotor_mappings[self.rotor_type][index:] + \
                                               self.rotor_mappings[self.rotor_type][:index]

        self.ring_positions[self.rotor_type] = self.ring_positions[self.rotor_type][index:] + \
                                               self.ring_positions[self.rotor_type][:index]

        self.ring_main[self.rotor_type] = self.ring_main[self.rotor_type][index:] + \
                                          self.ring_main[self.rotor_type][:index]

    # Instance method to encode letter from right to left (pins to contacts)
    def encode_right_to_left(self, index):
        if type(index) == str:
            index = self.ring_main[self.rotor_type].index(index)
            return self.rotor_mappings[self.rotor_type][index]

        character = self.rotor_mappings[self.rotor_type][index]
        return self.ring_positions[self.rotor_type].index(character)

    # Instance method to encode letter from left to right (contacts to pins)
    def encode_left_to_right(self, index):
        if type(index) == str:
            index = self.rotor_mappings[self.rotor_type].index(index)
            return self.ring_main[self.rotor_type][index]

        character = self.ring_positions[self.rotor_type][index]
        return self.rotor_mappings[self.rotor_type].index(character)
