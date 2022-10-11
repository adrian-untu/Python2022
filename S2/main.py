# 1. Write a function to return a list of the first n numbers in the Fibonacci string.
def function1(n):

    if not n:
        return [0]
    if n == 1:
        return [0, 1]
    list_of_fib = [0, 1]
    for i in range(2, n):
        list_of_fib.append(list_of_fib[i-1] + list_of_fib[i-2])

    return list_of_fib


def function1_get_n_elem(n):
    from math import sqrt
    return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))

# 2. Write a function that receives a list of numbers and returns a list of the prime numbers found in it.
def function2(list_of_nr):
    return [x for x in list_of_nr if len([d for d in range(2, (x//2 + 1)) if x % d == 0]) == 0]

# 3. Write a function that receives as parameters two lists a and b and returns: (a intersected with b, a reunited with b, a - b, b - a)
def function3(list1, list2):

    list_intersect = []
    list_first_minus_second = []
    list_second_minus_first = []
    list_reunion = []
    for item1 in list1:
            if item1 in list2 and item1 not in list_intersect:
                list_intersect.append(item1)
    for item1 in list1:
        if item1 not in list2:
            list_first_minus_second.append(item1)
    for item2 in list2:
        if item2 not in list1:
            list_second_minus_first.append(item2)
    for item1 in list1:
        if item1 not in list_reunion:
            list_reunion.append(item1)
    for item2 in list2:
        if item2 not in list_reunion:
            list_reunion.append(item2)

    return list_intersect, list_reunion, list_first_minus_second, list_second_minus_first

# 4. Write a function that receives as a parameters a list of musical notes (strings), a list of moves (integers) and a start position (integer).
# The function will return the song composed by going though the musical notes beginning with the start position and following the moves given as parameter.
#    Example : compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2) will return ["mi", "fa", "do", "sol", "re"]
def function4(musical_notes, list_of_moves, start_position):

    new_list = [musical_notes[start_position]]

    for move in list_of_moves:
        if move < 0:
            start_position -= (move + 1)
            start_position = start_position % len(musical_notes)
        else:
            start_position = start_position + move
            start_position = start_position % len(musical_notes)
        new_list.append(musical_notes[start_position])
    return new_list

# 5. Write a function that receives as parameter a matrix and will return the matrix obtained by replacing all the elements under the main diagonal with 0 (zero).
def function5(matrix):

    for l in range(len(matrix)):
        for c in range(l):
            matrix[l][c] = 0
    return matrix

# 6. Write a function that receives as a parameter a variable number of lists and a whole number x. Return a list containing the items
# that appear exactly x times in the incoming lists.
# Example: For the [1,2,3], [2,3,4],[4,5,6], [4,1, "test"] and x = 2 lists [1,2,3 ] # 1 is in list 1 and 4, 2 is in list 1 and 2, 3 is in lists 1 and 2.
def function6(*lists):
    count = 2
    all_lists = []
    return_list = []
    for lst in lists:
        all_lists+=lst
    for item in all_lists:
        if all_lists.count(item) == count and item not in return_list:
            return_list.append(item)

    return return_list

# 7. Write a function that receives as parameter a list of numbers (integers) and will return a tuple with 2 elements.
# The first element of the tuple will be the number of palindrome numbers found in the list and the second element will be the greatest palindrome number.
def function7(lst_of_numbers):

    list_of_palindroms = [el for el in lst_of_numbers if str(el) == str(el)[::-1]]
    return tuple((len(list_of_palindroms), max(list_of_palindroms)))

# 8. Write a function that receives a number x, default value equal to 1, a list of strings, and a boolean flag set to True.
# For each string, generate a list containing the characters that have the ASCII code divisible by x if the flag is set to True,
# otherwise it should contain characters that have the ASCII code not divisible by x.
# Example: x = 2, ["test", "hello", "lab002"], flag = False will return (["e", "s"], ["e" . Note: The function must return list of lists.
def function8(*list_of_strings):
    x = 2
    flag = False
    return_list = []
    for string in list_of_strings:
        if flag:
            return_list.append([ch for ch in string if ord(ch) % x == 0])
        else:
            return_list.append([ch for ch in string if ord(ch) % x != 0])

    return return_list

# 9. Write a function that receives as paramer a matrix which represents the heights of the spectators in a stadium
# and will return a list of tuples (line, column) each one representing a seat of a spectator which can't see the game.
# A spectator can't see the game if there is at least one taller spectator standing in front of him. All the seats are occupied.
# All the seats are at the same level. Row and column indexing starts from 0, beginning with the closest row from the field.
# Example:
# # FIELD
# [[1, 2, 3, 2, 1, 1],
# [2, 4, 4, 3, 7, 2],
# [5, 5, 2, 5, 6, 4],
# [6, 6, 7, 6, 7, 5]]
# Will return : [(2, 2), (3, 4), (2, 4)]
def function9(matrix):

    list_of_positions = []
    matrix_transpose = list(zip(*matrix))

    for c in range(len(matrix_transpose)):
        for l in range(1, len(matrix_transpose[0])):
            if matrix_transpose[c][l] <= max(matrix_transpose[c][:l]):
                list_of_positions.append(tuple((l, c)))
    return list_of_positions

# 10. Write a function that receives a variable number of lists and returns a list of tuples as follows:
# the first tuple contains the first items in the lists, the second element contains the items on the position 2 in the lists, etc.
# Ex: for lists [1,2,3], [5,6,7], ["a", "b", "c"] return: [(1, 5, "a ") ,(2, 6, "b"), (3,7, "c")].
# Note: If input lists do not have the same number of items, missing items will be replaced with None to be able to
# generate max ([len(x) for x in input_lists]) tuples.
def function10(*lists):

    max_nr_of_elements = max([len(x) for x in lists])
    new_lists = [l+[None for i in range(len(l), max_nr_of_elements)] for l in lists]

    return list(zip(*new_lists))

# 11. Write a function that will order a list of string tuples based on the 3rd character of the 2nd element in the tuple.
# Example: [('abc', 'bcd'), ('abc', 'zza')] ==> [('abc', 'zza'), ('abc', 'bcd')]
def function11(lists):

    if len([l for l in lists if len(l) < 2]) != 0:
        print("Not valid list")
        return
    return sorted(lists, key=lambda i: i[1][2])
# 12. Write a function that will receive a list of words  as parameter and will return a list of lists of words, grouped by rhyme.
# Two words rhyme if both of them end with the same 2 letters.
# Example:
# group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']) will return [['ana', 'banana'], ['carte', 'parte'], ['arme']]
def function12(list):
    new_list = []
    for word in list:
        small_list = []
        last_2_chars = word[-1] + word[-2]
        #list.remove(word)
        for word2 in list:
            last_2_chars_second = word2[-1] + word2[-2]
            if last_2_chars_second == last_2_chars:
                small_list += [word2]
               # list.remove(word2)
        if new_list.count(small_list) == 0:
            new_list += [small_list]
    return new_list


if __name__ == '__main__':
    print(function1(3))
    print(function2([1,2,3,4,5]))
    print(function3([2,5,4,8], [1,2,3,4]))
    print(function4(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
    print(function5([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(function6([1,2,3], [2,3,4],[4,5,6], [4,1, "test"]))
    print(function7([12321, 23432, 123, 4567654]))
    print(function8("test", "hello", "lab002"))
    print(function9([[1, 2, 3, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5]]))
    print(function10([1,2,3], [5,6,7], ["a", "b", "c"]))
    print(function11([('abc', 'bcd'), ('abc', 'zza')]))
    print(function12(['ana', 'banana', 'carte', 'arme', 'parte']))
