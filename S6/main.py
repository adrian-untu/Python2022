import os
import re

# 1) Write a function that extracts the words from a given text as a parameter. A word is defined as a sequence of alphanumeric characters.
def function1(text):
    return re.findall("[a-z0-9]+",text,flags=re.IGNORECASE)

# 2) Write a function that receives as a parameter a regex string,
# a text string and a whole number x, and returns those long-length x substrings that match the regular expression.
def function2(r,text,x):
    return list(filter(lambda el:len(el)==x, re.findall(r,text)))

# 3) Write a function that receives as a parameter a string of text characters and a list of regular expressions
# and returns a list of strings that match on at least one regular expression given as a parameter.
def function3(text_chars,list_of_re):
    return [el for el in text_chars if any([re.search(r,el) for r in list_of_re])]

# 4) Write a function that receives as a parameter the path to an xml document and an attrs dictionary and returns those elements
# that have as attributes all the keys in the dictionary and values ​​the corresponding values. For example,
# if attrs={"class": "url", "name": "url-form", "data-id": "item"} the items selected will be those tags whose attributes
# are class="url" si name="url-form" si data-id="item".
def function4(path_to_xml,attrs):
    result = []
    with open(path_to_xml,"r") as f_d:
        for el in re.findall("<\w+.*?>",f_d.read()):
            if(all([re.search(item[0]+"\s*=\s*\""+item[1] + "\"",el,flags=re.I) for item in attrs.items()])):
                result+=[el]
    return result

# 5) Write another variant of the function from the previous exercise that returns those elements that have at
# least one attribute that corresponds to a key-value pair in the dictionary.
def function5(path_to_xml, attrs):
    result = []
    with open(path_to_xml, "r") as f_d:
        for el in re.findall("<\w+.*?>", f_d.read()):
            if (any([re.search(item[0] + "\s*=\s*\"" + item[1] + "\"", el, flags=re.I) for item in attrs.items()])):
                result += [el]
    return result

# 6) Write a function that, for a text given as a parameter, censures words that begin and end with vowels.
# Censorship means replacing characters from odd positions with *.
def censor(s):
    low_s = s.group(0).lower()
    if not (low_s[0] in "aeiou" and low_s[-1] in "aeiou"):
        return s.group(0)
    return "".join([ch if idx%2 == 0 else '*' for idx,ch in enumerate(s.group(0))])

def function6(text):
    return re.sub("\w+", censor, text)

# 7) Verify using a regular expression whether a string is a valid CNP.
def function7(cnp):
    if len(cnp) == 13:
        if re.match(r"[1256]\d\d(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{6}$",cnp):
            return "YES"
    return "NO"

# 8) Write a function that recursively scrolls a directory and displays those files whose name
# matches a regular expression given as a parameter or contains a string that matches the same expression.
# Files that satisfy both conditions will be prefixed with ">>"
def function8(directory,reg):
    result = []
    for root,dirs,files in os.walk(directory):
        for f in files:
            file_name = os.path.join(root,f)
            r = re.search(reg,f)
            if r:
                result += [f]
            try:
                with open(file_name, "r") as f_d:
                        string = f_d.read()
                        if (re.search(reg, string)):
                            if r:
                                result[-1] = ">>" + result[-1]
                            else:
                                result+=[f]
            except:
                pass
    return result

if __name__ == '__main__':
    print(str(function1("hello my friend I am ready to be ready")))
    print(str(function2("a", "hello my friend I am ready to be ready", 1)))
    print(str(function3("hello my friend I am ready to be ready",["a","b","e"])))
    print(str(function4("D:\Facultate anul 3\PP (Programare in Python)\FileTests\S6\example.xml", attrs={"class": "url", "name": "url-form", "data-id": "item"})))
    print(str(function5("D:\Facultate anul 3\PP (Programare in Python)\FileTests\S6\example.xml", attrs={"class": "url", "name": "url-form", "data-id": "item"})))
    print(str(function6("apple are made from an apple tree")))
    print(str(function7("5010728236803")))
    print(str(function8("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S6", "m")))