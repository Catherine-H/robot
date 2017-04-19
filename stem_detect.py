import numpy as np
import cv2

# HSV color thresholds for RED
THRESHOLD_LOW_R1 = (0, 70, 50)
THRESHOLD_HIGH_R1 = (4, 255, 255)

# HSV color thresholds for RED
THRESHOLD_LOW_R2 = (171, 70, 50)
THRESHOLD_HIGH_R2 = (178, 255, 255)

# Minimum required radius of enclosing circle of contour
MIN_RADIUS = 10

# Initialize camera
cam = cv2.VideoCapture(0)
widthMoy = 0
thetaMoy = 0
moy = 0
# Main loop
while True:

    # Get image from camera
    ret_val, img = cam.read()

    # Erase image to remove noise
    img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)

    # Convert image from BGR to HSV
    img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

    # Set pixels to white if in color range (binary bitmap) for each color
    img_binary_R1 = cv2.inRange(img_filter.copy(), THRESHOLD_LOW_R1, THRESHOLD_HIGH_R1)
    img_binary_R2 = cv2.inRange(img_filter.copy(), THRESHOLD_LOW_R2, THRESHOLD_HIGH_R2)

    # Gathers all binary bitmap
    img_binary = img_binary_R2 + img_binary_R1

    # Find center of object using contours
    img_contours = img_binary.copy()
    contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE)[-2]
    tt = 0

    # Find the largest contour
    for cnt in contours:
        if tt == 0:
            x, y, w, h = cv2.boundingRect(cnt)
            if h > 20:
                tt = 1
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

                # => rect =  (x,y),(width,height),theta
                rect = cv2.minAreaRect(cnt)

                #width || heigth ==> prendre le rectangle dans le bon sens
                if (rect[1][1]) <= (rect[1][0]):
                    width = rect[1][1]

                else:
                    width = rect[1][0]

                #dessiner rectangle bleu
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, (255, 0, 0), 1)


                if (moy < 5):
                    widthMoy = widthMoy + width
                    thetaMoy = thetaMoy + rect[2]
                    moy += 1
                elif (moy == 5):
                    widthMoy = widthMoy/moy
                    thetaMoy = thetaMoy/moy
                    #print widthMoy
                    #print str(widthMoy) + "        " + str(thetaMoy) #theta
                    distance = 9 * 30 / widthMoy
                    print str(widthMoy) + "        " + str(distance)
                    moy = 0
                    widthMoy = 0
                    thetaMoy = 0

    # Show image windows
    cv2.imshow('webcam', img)
    cv2.imshow('binary', img_binary)
    cv2.imshow('contours', img_contours)
    cv2.waitKey(1)