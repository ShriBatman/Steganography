import cv2

def toBinary(arr):
    a,b,c = arr
    return ('{0:08b}'.format(a),'{0:08b}'.format(b),'{0:08b}'.format(c))

def toInteger(arr):
    a,b,c = arr
    return (int(a,2),int(b,2),int(c,2))

def encode(cover,conceal):
    cov = cv2.imread(cover)
    con = cv2.imread(conceal)

    h1,w1 = cov.shape[:2]
    h2,w2 = con.shape[:2]

    if h1<h2 or w1<w2:
        return -1

    for i in range(h1):
        for j in range(w1):
            x1,y1,z1 = toBinary(cov[i,j])
            x2,y2,z2 = toBinary((0,0,0))

            if i<h2 and j<w2:
                x2,y2,z2 = toBinary(con[i,j])

            new = (x1[:4]+x2[:4],y1[:4]+y2[:4],z1[:4]+z2[:4])
            new = toInteger(new)
            cov[i,j] = new
    cv2.imwrite("K:\\image_encoded.png",cov)
    return 1

def decode(image):
    img = cv2.imread(image)

    h,w = img.shape[:2]
    u=0
    v=0

    for i in range(h):
        for j in range(w):
            x,y,z = toBinary(img[i,j])
            arr = (x[4:]+"0000",y[4:]+"0000",z[4:]+"0000")

            new = toInteger(arr)
            img[i,j] = new 

            if new != (0,0,0):
                u=i+1
                v=j+1

    new_img = img[0:u,0:v]
    cv2.imwrite("k:\\orignal_image.png",new_img)
    return 1

    
