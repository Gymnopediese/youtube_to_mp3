from ALIBKL.string.rm_from_to import remove_from_to

def valid_title(titles, blacklist, index):
    if (index < 0):
        return "nobody"
    titles[index] = remove_from_to(titles[index], "(", ")")
    for i in titles[index].split(" "):
        if i.lower() in blacklist:
            return valid_title(titles, blacklist, index - 1)
    return titles[index]

def blacklist():
    blacklist = "Audio Clip Documentaire Officiel"
    list = blacklist.split(" ")
    for i in range(len(list)):
        list[i] = list[i].lower()
    return list

def clean_title(title):
    title = title.split(" - ")
    title = valid_title(title, blacklist(), len(title) - 1)
    if title[-1] == " ":
        title = title[:len(title) - 1]
    title = title.replace("/", "-")
    return title