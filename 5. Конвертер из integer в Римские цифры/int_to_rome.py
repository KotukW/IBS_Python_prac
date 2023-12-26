def int_to_roman(num):
    arab = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]

    rome = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // arab[i]):
            roman_num += rome[i]
            num -= arab[i]
        i += 1
    return roman_num

print(int_to_roman(32))  # Output: XXXII
print(int_to_roman(54))  # Output: LIV
print(int_to_roman(1984))  # Output: MCMLXXXIV
print(int_to_roman(2024)) # Output: MMXXIV   