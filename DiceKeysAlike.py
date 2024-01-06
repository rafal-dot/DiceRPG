#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DiceKeysAlike.py: Generate top quality passwords from all random factors that can be observed rolling dice: (i) dice
rolls, (ii) dice directions and (iii) order of dices. Concept os based on DiceKeys solution (for details see
https://dicekeys.com/)

https://github.com/rafal-dot/DiceRPG

Created on Fri Jan  5 19:26:10 2024
@author: Rafal Czeczotka <rafal dot czeczotka at gmail.com>

Copyright (c) 2024 Rafal Czeczotka

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see
<https://www.gnu.org/licenses/>.
"""

import re
from math import floor, ceil, log10, factorial
from permutation import Permutation

# Characters set for machine-storred, human-retyped passwords. For suggestions for (i) handwritten passwords or
# (ii) passwords stored and processed entirely by machine, see the documentation
ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%&()/?"
ALPHABET_LEN = len(ALPHABET)
# Faces are digits "1"-"6". 6 is translated to 0 in modulo operation
DICE_FACES = 6
# Convention used for directions can be: (i) "0123", (ii) "1234" or (iii) "NESW"/"nesw" (translated to "0123")
DICE_DIRECTIONS = 4

while True:
    print(f"""
Please enter random dice rolls (string of digits from 1 to 6), 67 characters alphabet
bits of entropy --->  49| 79|  |103      |195       |298
password length --->   8| 13|  |17       |32        |49
dice rolls --+----->    v 1 v  v    2    v    3     v
             +-> 123456789012345678901234567890123456""")
    dice_rolls_string = input("Dice rolls     : ")
    if dice_rolls_string == "":
        break
    dice_directions_string = input("Dice directions: ")
    dice_order_string = input("Dice order     : ")
    number_of_rolls = len(dice_rolls_string)

    # Calculate random part from order of dices (=rolls!)
    dices_order = [eval(i) for i in re.split("[-+*/=:;., ]", dice_order_string)]
    random_number = Permutation(*dices_order).lehmer(len(dices_order))

    # Calculate random part from rolls of dices (6^rolls)
    for roll_char in dice_rolls_string:
        random_number = DICE_FACES * random_number + (eval(roll_char) % DICE_FACES)

    # Calculate random part from directions of dices (4^rolls)
    dice_directions_string = dice_directions_string.translate(str.maketrans("NESWnesw", "01230123"))
    for direction_char in dice_directions_string:
        random_number = DICE_DIRECTIONS * random_number + (eval(direction_char) % DICE_DIRECTIONS)

    effective_password_len = floor(
        log10(factorial(number_of_rolls) * (DICE_FACES * DICE_DIRECTIONS) ** number_of_rolls) / log10(ALPHABET_LEN)
    )
    bits_of_entropy = ceil(effective_password_len * log10(ALPHABET_LEN) / log10(2))
    password = ""
    for _ in range(effective_password_len):
        password = ALPHABET[random_number % ALPHABET_LEN] + password
        random_number = random_number // ALPHABET_LEN

    print(f"\nRolls of dice: {number_of_rolls}    Entropy: {bits_of_entropy} bits"
          f"   Length of password ({ALPHABET_LEN} chars alphabet): {effective_password_len}")
    print(f"Password: \"{password}\"")
