import datetime


def decode(arr: bytes):
    """Decode array of bytes to form for db
    :param arr: 24 bytes from com port
    :return: collection of data
    """
    arr_rays = []
    rays = ''
    k = 0
    for i in range(1, 19):
        if arr[i] & 0b11000000 == 0b11000000:
            rays += 'n'
        else:
            rays += 'o'
        if arr[i] & 0b00110000 == 0b00110000:
            rays += 'n'
        else:
            rays += 'o'
        if arr[i] & 0b00001100 == 0b00001100:
            rays += 'n'
        else:
            rays += 'o'
        if arr[i] & 0b00000011 == 0b00000011:
            rays += 'n'
        else:
            rays += 'o'

    data = {'address': arr[0],
            'rays': rays,
            'power': (arr[19] & 0b01110000) >> 4,
            'configuration': arr[19] & 0b00001111,
            'volt': arr[20]/10 - 5,
            'rele': (arr[21] & 0b10000000) >> 7,
            'time': datetime.datetime.now()
            }
    return data


def decode_multi(arr):
    data = []
    for i in range(0, len(arr)):
        data.append(decode(arr[i]))
    return data
