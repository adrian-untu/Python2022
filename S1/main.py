import re


# 1 Find The greatest common divisor of multiple numbers read from the console.
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def multiple_gcd(*nr):
    a = gcd(nr[0], nr[1])
    for i in range(2, len(nr)):
        a = gcd(nr[i], a)
    return a


print("1: \n GCD of the entered numbers: " + str(multiple_gcd(16, 20, 36, 8)))


# 2 Write a script that calculates how many vowels are in a string.
def number_of_vowels(string):
    nr_of_vowels = 0
    for letter in string:
        if letter in 'aeiouAEIOU':
            nr_of_vowels += 1
    return nr_of_vowels


print("2: ")
string = input("Enter word: ")
print("Number of vowels for input string: " + str(number_of_vowels(string)))

# 3 Write a script that receives two strings and prints the number of occurrences of the first string in the second.

def count(s1, s2):
    counter = 0
    while(s1):
        if s1.startswith(s2):
            counter = counter + 1
            s1 = s1[len(s2):]
        else:
            s1 = s1[1:]
    return counter
print("3: ")
s1 = input("Enter origin script: ")
s2 = input("Enter separator: ")
print(count(s1, s2))

# 4 Write a script that converts a string of characters written in UpperCamelCase into lowercase_with_underscores.

print("4 :")
s1 = input("Enter UpperCamelCase string: ")
s2 = re.sub(r'(?<!^)(?=[A-Z])', '_', s1).lower()
print("lowercase_with_underscores string: " + s2)


# 5 Given a square matrix of characters, write a script that prints the string obtained by going through the matrix in spiral order

def spiralOrder(matrix):
    ans = []

    if len(matrix) == 0:
        return ans

    m = len(matrix)
    n = len(matrix[0])
    seen = [[0 for i in range(n)] for j in range(m)]
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    x = 0
    y = 0
    di = 0

    # Iterate from 0 to R * C - 1
    for i in range(m * n):
        ans.append(matrix[x][y])
        seen[x][y] = True
        cr = x + dr[di]
        cc = y + dc[di]

        if (0 <= cr and cr < m and 0 <= cc and cc < n and not (seen[cr][cc])):
            x = cr
            y = cc
        else:
            di = (di + 1) % 4
            x += dr[di]
            y += dc[di]
    return ans


print("5: ")

a = [["f", "i", "r", "s"],
     ["n", "_", "l", "t"],
     ["o", "b", "a", "_"],
     ["h", "t", "y", "p"]]
for x in spiralOrder(a):
    print(x, end="")

# 6 Write a function that validates if a number is a palindrome.

def check_palindrome (number):
    check = 0
    copy_number = number
    while copy_number:
        check = check * 10 + copy_number % 10
        copy_number = copy_number // 10
    if check == number:
        return "EGAL"
    else:
        return "NOT EGAL"

print("6: ")
number = int(input("Enter number for validation of palindrome: "))
print(check_palindrome(number))

# 7 Write a function that extract a number from a text (for example if the text is "An apple is 123 USD",
# this function will return 123, or if the text is "abc123abc" the function will extract 123).
# The function will extract only the first number that is found.

def extract_number(string):
    first_number = -1
    for i in range (len(string)-1):
        if string[i].isnumeric():
            first_number = 0
            first_number = first_number * 10 + int(string[i])
            i = i + 1
            while string[i].isnumeric():
                first_number = first_number * 10 + int(string[i])
                i = i + 1
            return first_number

print("7: ")
string = input ("Enter string for checking numbers: ")
first_number = extract_number(string)
if first_number == -1:
    print("No number found in string")
else:
    print("First number found in string: " + str(first_number))

# 8 Write a function that counts how many bits with value 1 a number has. For example for number 24,
# the binary format is 00011000, meaning 2 bits with value "1"

def check_bits_one (number):
    counter = 0
    while number:
        while number:
            counter += number & 1
            number >>= 1
    return counter

print("8: ")
number = int(input("Enter number here for counting bits with value '1': "))
number_of_bits = check_bits_one(number)
print("Total bits with value '1': " + str(number_of_bits))

# 9 Write a functions that determine the most common letter in a string.
# For example if the string is "an apple is not a tomato", then the most common character is "a" (4 times).
# Only letters (A-Z or a-z) are to be considered. Casing should not be considered "A" and "a" represent the same character.

def most_frequent (string):
    all_freq = {}
    for i in string:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    res = max(all_freq, key=all_freq.get)
    return res

print("9: ")
string = input("Enter string for most frequent character: ")
print("The most frequent character is " + most_frequent(string))

# 10 Write a function that counts how many words exists in a text.
# A text is considered to be form out of words that are separated by only ONE space.
# For example: "I have Python exam" has 4 words.

def number_of_words (string):
    split_string = string.split(" ")
    length = len(split_string)
    return length

print("10: ")
string = input("Enter string for number of words: ")
print("Number of words in string is " + str(number_of_words(string)))