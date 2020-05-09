# Paweł Kajanek

import random
import crc8


alph = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def divide_packages(stream, frame_len=7) -> list:
    """Devides given stream into list of strings
    Parameters:
    stream (str): will be devided into smaller strings of given length
    frame_len (int): length of returned substrings 
    """

    return [stream[i:i+frame_len] for i in range(0, len(stream), frame_len)]


def crc(stream) -> str:
    """Returns crc8 for given string"""

    return bin(int(crc8.crc8(stream.encode('utf-8'))
            .hexdigest(), 16))[2:].zfill(8)


def pack(p) -> str:
    """Returns framed message with crc
    Parameters:
    p (str): message that will be framed
    """

    # Stworzenie crc
    c = crc(p)
    p = [bin(e.encode('utf-8')[0])[2:].zfill(8) for e in p]
    p = ''.join(p)
    p += c
    
    # 'Rozpychanie' bitów
    ret = ''
    for i in p:
        ret += i
        if ret.endswith('011111'):
            ret += '0'

    # Dodanie ramki
    ret += '01111110'
    ret = '01111110' + ret
    return ret


def unpack(p) -> str:
    """Returns message from frame
    Parameters:
    p (str): framed message
    """

    # 'Zdejmowanie' ramki
    p = p.replace('01111110', '')
    p = p.replace('01111110', '')
    
    # 'Spychanie' bitów
    ret = ''
    flag = False
    for i in p:
        ret += i
        if ret.endswith('0111110') and not flag:
            ret = ret[:-1]
            flag = True
        else:
            flag = False

    # Sprawdzenie crc
    c = ret[-8:]
    ret = [chr(int(ret[i:i+8],2)) for i in range(0, len(ret), 8)]
    ret = ''.join(ret[:-1])
    if crc(ret) == c:
        return ret
    else:
        return 0


def make_z(name='Z.txt', count=100):
    """Makes file with random characters
    Parameters:
    name (str, optional): path to the new file
    count (int, optional): number of characters created in the file
    """

    f = open(name, 'w')
    text = ''.join([random.choice(alph) for i in range(count)])
    f.write(text)
    f.close()


def readfile(z) -> str:
    """Returns content of file z
    Parameters:
    z (str): path of the file
    """

    f = open(z, 'r')
    raw = f.read()
    f.close()
    return raw


def save(tab, name, seperator = ''):
    """ Saves strings in tab to file
    Parameters:
    tab (list): string to save,
    name (str): filename
    seperator (str, optional): seperates elements of tab in the file
    """

    f = open(name, 'w')
    for p in tab:
        if p == 0:
            f.write('\'ERR\'')
        else:    
            f.write(p)
    f.close()


def main():
    """Example program"""

    make_z()
    stream = readfile('Z.txt')
    packages = divide_packages(stream)
    
    print(packages)

    temp = []
    for p in packages:
        temp.append(pack(p))
    
    save(temp, 'W.txt', seperator='\n')
    print(temp)

    temp2 = []
    for p in temp:
        temp2.append(unpack(p))
    
    save(temp2, 'Z2.txt')
    print(temp2)


if __name__ == "__main__":
    main()