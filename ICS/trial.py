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

PT = [1, 1, 1, 1, 0, 0, 1, 1]

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
    K1 = keyOrder(LS1+LS2, p8)
    LS1 = leftShift(2, LS1)
    LS2 = leftShift(2, LS2)
    K2 = keyOrder(LS1+LS2, p8)
    return K1, K2

def XOR (a, b):
    return [int(a[i]) ^ int(b[i]) for i in range(len(a))]

def matrix(m, text):
    row = int(str(text[0]) + str(text[3]), 2)
    col = int(str(text[1]) + str(text[2]), 2)
    return m[row][col]

def F(text, k):
    l1, r1 = split(text)
    EP_op = keyOrder(EP, r1)
    XOR_op = XOR(EP_op, k)
    l2, r2 = split(XOR_op)
    matrix_op = matrix(S0, [l2[0], l2[3], l2[1], l2[2]]) + matrix(S1, [r2[0], r2[3], r2[1], r2[2]])
    P4_op = keyOrder(P4, matrix_op)
    XOR_op = XOR(l1, P4_op)
    return XOR_op, r1

def SDES():
    k1, k2 = genKeys()
    ip = keyOrder(IP, PT)
    a, b = F(ip, k1)
    c, d = F(b + a, k2)
    inv_op = keyOrder(IPinv, c + d)
    
    print(inv_op)

SDES()
