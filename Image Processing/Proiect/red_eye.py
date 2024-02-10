# imports
import cv2
import numpy as np

# read image
img = cv2.imread("input.jpg")

# make a copy in the result image
result_image = img.copy()

# eye detection and draw a rectangle around them
# eyes detected using CascadeClassifier from opencv
eyesCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
eyeRects = eyesCascade.detectMultiScale(img, 1.1, 5)
# scaleFactor = 1.1 always
# minNeighbors = 5 for valdiation of detected eyes

# we have the eyes with x, y (top left corner position), w(width), h(height) characteristics
for x, y, w, h in eyeRects:
    # center of the eye region
    center_x = x + w / 2
    center_y = y + h / 2

    # size of the croped image
    crop_width = 100
    crop_height = 100

    # coordinates of the top left corner of the cropped image and check for image boundaries
    crop_x = int(center_x - crop_width / 2)
    crop_y = int(center_y - crop_height / 2)
    crop_x = max(crop_x, 0)
    crop_y = max(crop_y, 0)

    eyeImage = img[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

    # blue, green, red channels
    b, g, r = cv2.split(eyeImage)
    
    # element-wise addition of blue and gree
    # ex b = 75, g = 25 for a pixel
    # => bg = 100
    bg = cv2.add(b, g)

    # red region mask construction
    # check if red bigger than bg - 20 and
    # if red bigger than 80
    # returns boolean value
    # so cast it to uint8
    # if both conditions satisfied => 255
    # else => 0
    mask = ((r > (bg - 20)) & (r > 80)).astype(np.uint8) * 255

    # get the contours in the masked image
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # we don't care about hierarchy

    # on the masked image we need to find the contour with the biggest area
    max_area = 0
    max_contour = None
    
    for contour in contours:
        
        area = cv2.contourArea(contour)
        
        if area > max_area:
            max_area = area
            max_contour = contour

    # make the image black again so that we can draw the contour again
    # this is done by reseting the mask
    mask = mask & 0

    # draw the biggest contour
    cv2.drawContours(mask, max_contour, 0, 255, -1)

    # make the region smooth
    # dilation and erosion with 5x5 structural element
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_DILATE, (5, 5)))
    mask = cv2.dilate(mask, (3, 3), iterations = 3)

    # fill the eye with the mean of blue and green
    mean = bg / 2

    # mask the mean
    mean = cv2.bitwise_and(mean, mask)

    # make mean and mask coloured images
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mean = cv2.cvtColor(mean, cv2.COLOR_GRAY2BGR)

    # ~mask => mask reprezenting the background
    # the bitwise and masks out the background regions
    # add the mean to show the colour
    eye_image = cv2.bitwise_and(~mask, eye_image) + mean

    result_image [y : y + h, x : x + w] = eye_image

cv2.imshow("Input", img)
cv2.imshow("Output", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

