import cv2

def matrix(key):
        mat = []
        for k in key.upper():
                #print ord(k)
                if k not in mat and ord(k) > 64 and ord(k) < 91:
                        mat.append(k)

        alphabets = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        for x in alphabets:
                if x not in mat:
                        mat.append(x)   
        
        matrix = []
        i = 0
        for x in range(5):
                matrix.append(mat[i:i+5])
                i = i+5
                
        return matrix

def toMDigraphs(mes):
        message = []
        for x in mes:
                message.append(x)

        for i in range(len(message)):
                if " " in message:
                        message.remove(" ")
        for i in range(len(message)):                
                if message[i] == 'j':
                        message.remove("j")
                        message.insert(i,'I')
        i = 0
        while i < len(message)-1:
                if message[i] == message[i+1]:
                        message.insert(i+1,'X')
                i = i+2

        if len(message)%2 == 1:
                message.append("X")

        i = 0
        new = []
        for x in xrange(1,len(message)/2+1):
                new.append(message[i:i+2])
                i = i+2
        return new

def pos(key_mat,letter):
        
        for i in range(5):
                for j in range(5):
                        if key_mat[i][j] == letter.upper():
                                return i,j

def Encrypt(text):
        message = toMDigraphs(text)
        #print message
        key_mat = matrix(key)
        #print key_mat
        cipher = []
        for i in message:
                x1,y1 = pos(key_mat,i[0])
                x2,y2 = pos(key_mat,i[1])
                #print x1,y1,x2,y2
                if x1 == x2:
                        if y1 == 4:
                                y1 = -1
                        if y2 == 4:
                                y2 = -1
                        cipher.append(key_mat[x1][y1+1])
                        cipher.append(key_mat[x2][y2+1])                
                elif y1 == y2:
                        if x1 == 4:
                                x1 = -1;
                        if x2 == 4:
                                x2 = -1;
                        cipher.append(key_mat[x1+1][y1])
                        cipher.append(key_mat[x2+1][y2])
                else:
                        cipher.append(key_mat[x1][y2])
                        cipher.append(key_mat[x2][y1])
        encrypt = ""
        for p in cipher:
                encrypt += p
        #print encrypt
        return encrypt

def toCDigraphs(cipher):
        i = 0
        new = []
        for x in range(len(cipher)/2):
                new.append(cipher[i:i+2])
                i = i+2
        return new


def Decrypt(cipher):    
        cipher = toCDigraphs(cipher)
        key_mat = matrix(key)
        #print key_mat
        text = []
        for k in cipher:
                x1,y1 = pos(key_mat,k[0])
                x2,y2 = pos(key_mat,k[1])
                if x1 == x2:
                        if y1 == 4:
                                y1 = -1
                        if y2 == 4:
                                y2 = -1
                        text.append(key_mat[x1][y1-1])
                        text.append(key_mat[x2][y2-1])          
                elif y1 == y2:
                        if x1 == 4:
                                x1 = -1;
                        if x2 == 4:
                                x2 = -1;
                        text.append(key_mat[x1-1][y1])
                        text.append(key_mat[x2-1][y2])
                else:
                        text.append(key_mat[x1][y2])
                        text.append(key_mat[x2][y1])
        original = ""
        for i in range(len(text)):
                if "X" in text:
                        text.remove("X")

        for p in text:
                original += p
        return original


def caesar_en(n, plaintext):
    result = ''

    for l in plaintext.lower():
        try:
            i = (key.index(l) + n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result.lower()

def caesar_de(n, ciphertext):
    result = ''

    for l in ciphertext:
        try:
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l
    return result

    """decode = open("decode.txt","w")
    decode.write(result)
    decode.close()"""


def toBinary(text):
    binary =[]
    for s in text:
        x = ord(s)
        pix = []
        i=0
        while(i<4):
            _two = x&3
            pix.append(_two)
            x=x>>2
            i=i+1
        binary.append(pix)
        
    return binary

def encode(img,arr):
    i=0
    p=0
    #while(i<len(arr2d)):
    while(i<len(img) and p<len(arr)):
        j=0
        while(j<len(img[0]) and p<len(arr)):
          #while(j<len(arr2d[0])):
            pix = img[i][j]
            hide = arr[p]
            p=p+1
            #hide = arr2d[i][j]
            k=0
            while(k<4):
                _two = pix[k] & 0b11111100
                pix[k] = _two | hide[k]
                k=k+1
            img[i][j] = pix
            j=j+1
        i=i+1
    return img
        
def stega(path,text):

    img = cv2.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2RGBA)

    """width = len(img)
    height = len(img)
    min=0

    if(width<height):
        min = width-3
    else:
        min = height-3

    min = int(min*min)"""
    arr = toBinary(text)
    #print arr

    """length = len(arr)
    print length
    sq_mat = length**(0.5)
    if(sq_mat>int(sq_mat)):
        sq_mat = int(sq_mat)+1

    #print sq_mat

    arr2d = []
    i = 0
    L = 0
    while(i<sq_mat):
        temp = []
        j = 0
        while(j<sq_mat):
            if(L<length):
                temp.append(arr[L])
                L = L+1
            else:
                temp.append([0,0,0,0])
            j=j+1
        arr2d.append(temp)
        i=i+1
    #print arr2d"""
    new_img = encode(img,arr)
    #for n in new_img[0]:
        #print n
    #print new_img[1]
    cv2.imwrite("encoded.png",new_img)
    #print "lkllkk"
    return 1
        

def toString(arr):
    #print arr
    str1 = ''
    for char in arr:
        i=0
        k=0
        for bits in char:
            k = k | bits<<(i*2)
            i=i+1
        #print k
        if(k == 3):
            break
        str1 = str1 + chr(k)
    return str1
            



    
def decode(path):
    img = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    #print "jhhhhhhhhg"
    #for i in img[0]:
        #print i
    #print img[1]
    hidden = []

    i=0
    while(i<len(img)):
        j=0
        #temp = []
        while(j<len(img[0])):
            _two = img[i][j] & 3
            hidden.append(_two)
            j=j+1
        #hidden.append(temp)
        i=i+1
    str11 = toString(hidden)
    return str11
    

            
key = "abcdefghijklmnopqrstuvwxyz"
play = 'IAMACONFLICTEDCONTRADICTION'
