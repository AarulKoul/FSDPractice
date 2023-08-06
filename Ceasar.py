while True:
    choice = int(input("Enter choice:\n1)Encrypt\n2)Decrypt\n3)Exit\n"))
    if choice == 1:
        key = int(input("Enter number of digits to shift: "))%26
        ptext = input("Enter message: ")
        ctext = ""
        for i in ptext:
            if (ord(i)>=97 and ord(i)<=122):
                if (ord(i)+key) > 122:
                    ctext = ctext+(chr(ord(i)+key-26))
                else:
                    ctext = ctext+chr(ord(i)+key)
            elif (ord(i)>=65 and ord(i)<=90):
                if (ord(i)+key) > 90:
                    ctext = ctext+(chr(ord(i)+key-26))
                else:
                    ctext = ctext+chr(ord(i)+key)
            else:
                ctext = ctext+i
                    
        print(ctext)

    elif choice == 2:
        dchoice = int(input("Enter choice:\n1)With Key\n2)Hack\n"))
        if dchoice == 1:
            key = int(input("Enter key: "))%26
            ctext = input("Enter encrypted message: ")
            ptext = ""
            for i in ctext:
                if (ord(i)>=97 and ord(i)<=122):
                    if (ord(i)-key) < 97:
                        ptext = ptext+(chr(ord(i)-key+26))
                    else:
                        ptext = ptext+chr(ord(i)-key)
                elif (ord(i)>=65 and ord(i)<=90):
                    if (ord(i)-key) > 90:
                        ptext = ptext+(chr(ord(i)-key+26))
                    else:
                        ptext = ptext+chr(ord(i)-key)
                else:
                    ptext = ptext+i
            print(ptext)
        else:
            ctext = input("Enter encrypted message: ")
            ptext = ""
            for key in range (1, 26):
                for i in ctext:
                    if (ord(i)>=97 and ord(i)<=122):
                        if (ord(i)-key) < 97:
                            ptext = ptext+(chr(ord(i)-key+26))
                        else:
                            ptext = ptext+chr(ord(i)-key)
                    elif (ord(i)>=65 and ord(i)<=90):
                        if (ord(i)-key) > 90:
                            ptext = ptext+(chr(ord(i)-key+26))
                        else:
                            ptext = ptext+chr(ord(i)-key)
                    else:
                        ptext = ptext+i
                print(ptext)
                correct = int(input("Correct? (1 - Yes, 2 - No)\n"))
                if correct == 1:
                    break
                ptext = ""
            
    else:
        break
