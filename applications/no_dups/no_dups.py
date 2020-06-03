def no_dups(s):
    counts = {}
    str = ""

    for word in s.split(" "):
        if word not in counts and word != "":
            counts[word] = 1
        elif word != "":
            counts[word] += 1

    for word in counts:
        str += f"{word} "

    return str.strip()



if __name__ == "__main__":
    print(no_dups(""))
    print(no_dups("hello"))
    print(no_dups("hello hello"))
    print(no_dups("cats dogs fish cats dogs"))
    print(no_dups("spam spam spam eggs spam sausage spam spam and spam"))
