sbox = [["9", "4", "A", "B"],
        ["D", "1", "8", "5"],
        ["6", "2", "0", "3"],
        ["C", "E", "F", "7"]]
InvSBox = [["A", "5", "9", "B"],
           ["1", "7", "8", "F"],
           ["6", "0", "2", "3"],
           ["C", "4", "D", "E"]]
mixMatrix = [["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"],
             ["0", "2", "4", "6", "8", "A", "C", "E", "3", "1", "7", "5", "B", "9", "F", "D"],
             ["0", "4", "8", "C", "3", "7", "B", "F", "6", "2", "E", "A", "5", "1", "D", "9"],
             ["0", "9", "1", "8", "2", "B", "3", "A", "4", "D", "5", "C", "6", "F", "7", "E"]]
rcon1 = "10000000"
rcon2 = "00110000"
key = "4AF5"

def getInput():
    UserInp = input("Enter hex plain text: ")
    if(len(UserInp) != 4):
        print("Invalid Input!")
        return getInput()
    return [int(x) for x in UserInp]

def htb(s, len):
    binary_string = bin(int(s, 16))[2:]
    return binary_string.zfill(len)

def bth(s):
    binary_string = hex(int(s, 2))[2:]
    return binary_string

def split(arr):
    n = len(arr)
    return arr[:n//2], arr[n//2:]

def rotNib(arr):
    n = len(arr)
    return arr[n//2:] + arr[:n//2]

def subNib(bits, matrix):
    left, right = split(bits)
    i1, j1 = split(left)
    i2, j2 = split(right)
    i1 = int(i1, 2)
    j1 = int(j1, 2)
    i2 = int(i2, 2)
    j2 = int(j2, 2)
    return matrix[i1][j1] + matrix[i2][j2]

def XOR (a, b):
    return "".join([str(int(a[i]) ^ int(b[i])) for i in range(len(a))])
    
def genKeys(key):
    keys = []
    binKey = htb(key, 16)
    w0, w1 = split(binKey)                                  
    keys.append(w0 + w1)                                                 # KEY 1
    w2 = XOR(XOR(w0, rcon1),htb(subNib(rotNib(w1), sbox), 8))
    w3 = XOR(w2, w1)
    keys.append(w2 + w3)                                                 # KEY 2
    w4 = XOR(XOR(w2, rcon2), htb(subNib(rotNib(w3), sbox), 8))
    w5 = XOR(w4, w3)
    keys.append(w4 + w5)                                                # KEY 3
    
    return keys

def saesEncrypt(p, keysArr):
    pt = htb(p, 16)
    round0 = XOR(pt, keysArr[0])                                        #ADD ROUND KEY
    left, right = split(round0)
    subOP = htb(subNib(left, sbox)+subNib(right, sbox), 16)             #SUBSTITUTE WITH S-BOX
    matrixed = [[subOP[0:4], subOP[8:12]], 
                [subOP[12:16], subOP[4:8]]]                             #MIX COLUMN
    MC_OP = [[0, 0], [0, 0]]
    MC_OP[0][0] = XOR(htb(mixMatrix[0][int(matrixed[0][0], 2)], 4), htb(mixMatrix[2][int(matrixed[1][0], 2)], 4))
    MC_OP[0][1] = XOR(htb(mixMatrix[0][int(matrixed[0][1], 2)], 4), htb(mixMatrix[2][int(matrixed[1][1], 2)], 4))
    MC_OP[1][0] = XOR(htb(mixMatrix[2][int(matrixed[0][0], 2)], 4), htb(mixMatrix[0][int(matrixed[1][0], 2)], 4))
    MC_OP[1][1] = XOR(htb(mixMatrix[2][int(matrixed[0][1], 2)], 4), htb(mixMatrix[0][int(matrixed[1][1], 2)], 4))
    MC_string = MC_OP[0][0] + MC_OP[1][0] + MC_OP[0][1] + MC_OP[1][1]
    addKey2 = XOR(MC_string, keysArr[1])
    left, right = split(addKey2)
    subOP = htb(subNib(left, sbox)+subNib(right, sbox), 16)
    shifted = subOP[0:4] + subOP[12:16] + subOP[8:12] + subOP[4:8]
    addKey3 = XOR(shifted, keysArr[2])
    return addKey3

def saesDecrypt(c, keysArr):
    ct = htb(c, 16)
    round0 = XOR(ct, keysArr[2])  
    shifted = round0[0:4] + round0[12:16] + round0[8:12] + round0[4:8]
    left, right = split(shifted)
    subOP = htb(subNib(left, InvSBox)+subNib(right, InvSBox), 16)
    round1 = XOR(subOP, keysArr[1])
    matrixed = [[round1[0:4], round1[8:12]], 
                [round1[4:8], round1[12:16]]]  
    MC_OP = [[0, 0], [0, 0]]
    MC_OP[0][0] = XOR(htb(mixMatrix[3][int(matrixed[0][0], 2)], 4), htb(mixMatrix[1][int(matrixed[1][0], 2)], 4))
    MC_OP[0][1] = XOR(htb(mixMatrix[3][int(matrixed[0][1], 2)], 4), htb(mixMatrix[1][int(matrixed[1][1], 2)], 4))
    MC_OP[1][0] = XOR(htb(mixMatrix[1][int(matrixed[0][0], 2)], 4), htb(mixMatrix[3][int(matrixed[1][0], 2)], 4))
    MC_OP[1][1] = XOR(htb(mixMatrix[1][int(matrixed[0][1], 2)], 4), htb(mixMatrix[3][int(matrixed[1][1], 2)], 4))
    MC_string = MC_OP[0][0] + MC_OP[1][0] + MC_OP[0][1] + MC_OP[1][1]
    shifted = MC_string[0:4] + MC_string[12:16] + MC_string[8:12] + MC_string[4:8]
    left, right = split(shifted)
    subOP = htb(subNib(left, InvSBox)+subNib(right, InvSBox), 16)
    round3 = XOR(subOP, keysArr[0])
    return round3
    
    
    

choice = 0
keys = genKeys(key)
while choice != "3":
    choice = input("Enter choice:\n1) Encrypt\n2) Decrypt\n3)Exit\n")
    if (choice == "1"):
        PT = input("Enter Hex Plain Text: ")
        print(f"Cipher Text: {bth(saesEncrypt(PT, keys)).upper()}")
    elif choice == "2":
        CT = input("Enter Hex Cipher Text: ")
        print(f"Plain Text: {bth(saesDecrypt(CT, keys)).upper()}")

