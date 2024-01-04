from os.path import exists

def input_filename(text):
    while (True):
        res = input(text)
        if " " not in res:
            return res
        else:
            print("not a valid filename: ")
def input_valid_file(text1, text2):
    while True:
        img = input(text1)
        if exists(img):
            return img
        else:
            print(text2)
def input_int(text1, text2):
    while True:
        img = input(text1)
        try:
            int(img)
            return int(img)
        except:
            print(text2)

def input_int_range(text1, text2, min, max):
    while True:
        img = input(text1)
        try:
            int(img)
            if not (int(img) < min or int(img) >= max):
                return int(img)
            print(text2)
        except:
            print(text2)
