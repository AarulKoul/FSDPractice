p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8 = [6,  3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IPinv = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2], 
      [3, 2, 1, 0], 
      [0, 2, 1, 3], 
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3], 
      [2, 0, 1, 3], 
      [3, 0, 1, 0], 
      [2, 1, 0, 3]]

key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]

def keyOrder(order, key):
    newOrder = []
    for i in range(len(order)):
        newOrder.append(key[order[i]-1])
    return newOrder

def leftShift(num, arr):
    return arr[num:] + arr[:num]

def split(arr):
    n = len(arr)
    return arr[:n//2], arr[n//2:]

def genKeys():
    P10 = keyOrder(p10, key)
    LS1, LS2 = split(P10)
    LS1 = leftShift(1, LS1)
    LS2 = leftShift(1, LS2)
    K1 = keyOrder(p8, LS1+LS2)
    LS1 = leftShift(2, LS1)
    LS2 = leftShift(2, LS2)
    K2 = keyOrder(p8, LS1+LS2)
    return K1, K2

def XOR (a, b):
    return [a[i] ^ b[i] for i in range(len(a))]

def matrix(m, text):
    row = int(str(text[0]) + str(text[3]), 2)
    col = int(str(text[1]) + str(text[2]), 2)
    b = bin(m[row][col]).replace("b", "")
    return list(map(int, [b[-2], b[-1]]))

def F(text, k):
    l1, r1 = split(text)
    EP_op = keyOrder(EP, r1)
    XOR_op = XOR(EP_op, k)
    l2, r2 = split(XOR_op)
    matrix_op = matrix(S0, l2) + matrix(S1, r2)
    P4_op = keyOrder(P4, matrix_op)
    XOR_op = XOR(l1, P4_op)
    return XOR_op, r1

def SDES_encrypt():
    k1, k2 = genKeys()
    ip = keyOrder(IP, PT)
    a, b = F(ip, k1)
    c, d = F(b+a, k2)
    inv_op = keyOrder(IPinv, c+d)
    
    return inv_op

def SDES_decrypt():
    k1, k2 = genKeys()
    ip = keyOrder(IP, CT)
    a, b = F(ip, k2)
    c, d = F(b+a, k1)
    inv_op = keyOrder(IPinv, c+d)
    
    return inv_op

def getInput():
    UserInp = input("Enter 8-bit plain text: ")
    if(len(UserInp) != 8):
        print("Invalid Input!")
        return getInput()
    return [int(x) for x in UserInp]

PT = getInput()
CT = SDES_encrypt()
Decrypted = SDES_decrypt()

print("\nCipher Text: ", end = "")
for i in CT:
    print(i, end=" ")

print("\nDecrypted Text: ", end = "")
for i in Decrypted:
    print(i, end=" ")
    
print("\n")