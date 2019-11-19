def sanatize(string, allow='abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLOMNOPQURSTUVWXYYZ1234567890'):
    sanatizedString = ''
    for char in string:
        if char in allow:
            sanatizedString += char
    return sanatizedString