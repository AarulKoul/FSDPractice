key = "VKILBTCXSJHNQPWAZFRUYDMEOG"
ptext = input("Enter message: ").lower()
ctext = ""
for i in ptext:
    if (ord(i)>=97 and ord(i)<=122):
        ctext = ctext+key[ord(i)-97]
    else:
        ctext = ctext+i
print(ctext)
