import numpy as np
import cv2

# HSV color thresholds for RED
THRESHOLD_LOW_R1 = (0, 170, 50)
THRESHOLD_HIGH_R1 = (4, 255, 255)

# HSV color thresholds for RED
THRESHOLD_LOW_R2 = (171, 170, 50)
THRESHOLD_HIGH_R2 = (178, 255, 255)

# HSV color threshold for GREEN
THRESHOLD_LOW_G = (45, 100, 50)
THRESHOLD_HIGH_G= (75, 255, 255)

# Minimum required radius of enclosing circle of contour
MIN_RADIUS = 10

# Initialize camera
cam = cv2.VideoCapture(0)


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
    img_binary_G = cv2.inRange(img_filter.copy(), THRESHOLD_LOW_G, THRESHOLD_HIGH_G)

    # Gathers all binary bitmap
    img_binary = img_binary_R2 + img_binary_G + img_binary_R1

    # Find center of object using contours
    img_contours = img_binary.copy()
    contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    # Find the largest contour
    center = None
    radius = 0
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < MIN_RADIUS:
                center = None

    # Print out the location and size (radius) of the largest detected contour
    if center != None:
        # Draw a green circle
        cv2.circle(img, center, int(round(radius)), (0, 255, 0))
        size = radius * 2
        distance = 70 * 41 / size

        print str(center) + "      " + str(distance)


    # Show image windows
    cv2.imshow('webcam', img)
    cv2.imshow('binary', img_binary)
    cv2.imshow('contours', img_contours)
    cv2.waitKey(1)