def zeros(int, amount = 2):
    int = str(int)
    while(len(int) < amount):
        int = "0" + int
    return int
