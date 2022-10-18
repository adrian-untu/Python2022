from collections.abc import Iterable
import json

# 1.Write a function that receives as parameters two lists a and b and returns a list
# of sets containing: (a intersected with b, a reunited with b, a - b, b - a)
def function1(a, b):
    return set(a) & set(b), set(a) | set(b), set(a) - set(b), set(b)-set(a)

# 2. Write a function that receives a string as a parameter and returns a dictionary
# in which the keys are the characters in the character string and the values are the
# number of occurrences of that character in the given text. Example: For string "Ana has apples."
# given as a parameter the function will return the dictionary: {'a': 3, 's': 2, '.': 1, 'e': 1,
# 'h': 1, 'l': 1, 'p': 2, ' ': 2, 'A': 1, 'n': 1} .
def function2(s):
    return {i: s.count(i) for i in set(s)}

# 3. Compare two dictionaries without using the operator "==" and return a list of differences
# as follows: (Attention, dictionaries must be recursively covered because they can contain
# other containers, such as dictionaries, lists, sets, etc.)
def return_elements(E):
    if isinstance(E, Iterable) and type(E) != str:
        values_list = []
        if type(E) == dict:
            for el in E.values():
                values_list += return_elements(el)
        else:
            for el in E:
                values_list += return_elements(el)
        return values_list
    return [E]


def function3(d1, d2):
    return list(set(return_elements(d1)) ^ set(return_elements(d2)))

# 4. The build_xml_element function receives the following parameters: tag, content,
# and key-value elements given as name-parameters. Build and return a string that
# represents the corresponding XML element. Example: build_xml_element ("a", "Hello there",
# href =" http://python.org ", _class =" my-link ", id= " some-id ") returns  the string =
# "<a href=\"http://python.org \ "_class = \" my-link \ "id = \" someid \ "> Hello there </a>"
def build_xml_element(tag, content, **parameters): #function4
    return "<" + tag + " " + r" ".join([p[0]+" = \"" + p[1] + "\"" if type(p[1]) == str else p[0]+" = " + str(p[1])
                                        for p in parameters.items()])+">"+content+"</"+tag+">"

# 5. The validate_dict function that receives as a parameter a set of tuples
# ( that represents validation rules for a dictionary that has strings as keys
# and values) and a dictionary. A rule is defined as follows: (key, "prefix",
# "middle", "suffix"). A value is considered valid if it starts with "prefix", "middle"
# is inside the value (not at the beginning or end) and ends with "suffix". The function
# will return True if the given dictionary matches all the rules, False otherwise. Example:
# the rules  s={("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}  and
# d= {"key1": "come inside, it's too cold out", "key3": "this is not valid"} => False
# because although the rules are respected for "key1" and "key2" "key3" that does not
# appear in the rules.
def validate_dict(rules, dictionary):
    rules = {rule[0]: [rule[1], rule[2], rule[3]] for rule in rules}
    return all([key in rules and value.startswith(rules[key][1]) and
                rules[key][2] in value and value.endswith(rules[key][3])
                for key, value in dictionary.items()])


# 6. Write a function that receives as a parameter a list and returns a tuple (a, b),
# representing the number of unique elements in the list, and b representing the number
# of duplicate elements in the list (use sets to achieve this objective).
def function6(list):
    return len(set(list)), len(list) - len(set(list))

# 7. Write a function that receives a variable number of sets and returns a dictionary
# with the following operations from all sets two by two: reunion, intersection, a-b, b-a.
# The key will have the following form: "a op b", where a and b are two sets, and op is the
# applied operator: |, &, -.
#
# Ex: {1,2}, {2, 3} =>
#
# {
#
#     "{1, 2} | {2, 3}": 3,
#![](C:/Users/untua/AppData/Local/Temp/image.webp)
#     "{1, 2} & {2, 3}": 1,
#
#     "{1, 2} - {2, 3}": 1,
#
#     ...
#
# }
def function7(*sets):
    finalresult = {}
    for idx1 in range(0, len(sets) - 1):
        for idx2 in range(idx1 + 1, len(sets)):
            finalresult.update({(str(sets[idx1]) + " | " + str(sets[idx2])): len((sets[idx1] | sets[idx2])),
                           (str(sets[idx1]) + " & " + str(sets[idx2])): len((sets[idx1] & sets[idx2])),
                           (str(sets[idx1]) + " - " + str(sets[idx2])): len((sets[idx1] - sets[idx2])),
                           (str(sets[idx2]) + " - " + str(sets[idx1])): len((sets[idx2] - sets[idx1]))})
    return finalresult

# 8. Write a function that receives a single dict parameter named mapping.
# This dictionary always contains a string key "start". Starting with the
# value of this key you must obtain a list of objects by iterating over mapping
# in the following way: the value of the current key is the key for the next value,
# until you find a loop (a key that was visited before). The function must return
# the list of objects obtained as previously described.
# Ex: loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})
# will return ['a', '6', 'z', '2']
def loop(map): #function8
    to_return = list()
    value = map['start']
    while value not in to_return:
        to_return.append(value)
        value = map[value]
    return to_return

# 9. Write a function that receives a variable number of positional
# arguments and a variable number of keyword arguments and will return
# the number of positional arguments whose values can be found among keyword
# arguments values.
# Ex: my_function(1, 2, 3, 4, x=1, y=2, z=3, w=5) will return 3
def function9(*arguments, **keywords):
    return len([e for e in arguments if e in keywords.values()])


#print all results of functions:
if __name__ == '__main__':
    print("PROBLEM 1: \n" + str(function1([1,2,3], [3,4,5])))
    print("PROBLEM 2: \n" + str(function2("Ana has apples")))
    f = open ('dict1.json', 'r')
    dict1 = json.load(f)
    f1 = open('dict2.json', 'r')
    dict2 = json.load(f1)
    print("PROBLEM 3: \n" + str(function3(dict1, dict2)))
    print("PROBLEM 4: \n" + str(build_xml_element ("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid ")))
    print("PROBLEM 5: \n" + str(validate_dict({("key1", "", "inside", ""), ("key2", "start", "middle", "winter")},  {"key1": "come inside, it's too cold out", "key3": "this is not valid"})))
    print("PROBLEM 6: \n" + str(function6([1,2,3,4,6,2,4,6,6,6,3,2])))
    print("PROBLEM 7: \n" + str(function7({1,2}, {2,3})))
    print("PROBLEM 8: \n" + str(loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})))
    print("PROBLEM 9: \n" + str(function9(1, 2, 3, 4, x=1, y=2, z=3, w=5)))