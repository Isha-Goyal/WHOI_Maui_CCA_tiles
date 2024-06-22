from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import numpy as np

im_path = '/home/igoyal/WHOI/WHOI_Maui_CCA_tiles/test_no_bkgd.png'
image = cv2.imread(im_path)
image = cv2.resize(image, (0, 0), fx = 0.1, fy = 0.1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 1, 200)

edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)


contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

contours = sorted(contours, key=lambda c: c[0][0][0], reverse=True)

cv2.imshow('window_name', image)
cv2.imshow('gray', gray)

# print("Number of Contours found = " + str(len(contours)))
cv2.imshow('Canny Edges After Contouring', edged)  

big = []
count = 0

for i,c in enumerate(contours):
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) > 1000: # note, might have to adjust this setup at the beginning to make sure you're getting two
		count+=1
		img = cv2.drawContours(image, c, -1, (255, 255, 255), 1)
		big.append(i)
		
print(count)

# if count != 2:
# 	print('could not find the correct number of contours')

# conts = [contours[i] for i in big]

# areas = cv2.drawContours(image, big, -1, (0, 255, 0), 3)
cv2.imshow('Large Area Edges', img) 
    

# find and assume right-most contour in image is reference (should be a circle of known size)
ref_cont = contours[big[1]]
ref_area_pixels = cv2.contourArea(ref_cont)
ref_diam_actual = 0.75 # actual diameter of your reference object (in whatever units)
ref_area_actual = np.pi * np.square(ref_diam_actual/2)
# ref_dia_pixels = np.sqrt(ref_area/np.pi) * 2
# ref_dia_actual = 20 # actual measurement of physical circular object's diameter
ratio = ref_area_actual/ref_area_pixels

cnts = cv2.drawContours(image, ref_cont, -1, (0,0,255), 3)


# print(ref_dia_pixels)
# print(ref_dia_actual)
# print('area of reference object: ' + str(ref_area_actual))
# print('ratio: ' + str(ratio))

# # find rect contour and say size
target_cont = contours[big[0]]
target_area_pixels = cv2.contourArea(target_cont)
target_area_actual = target_area_pixels * ratio
# print(target_cont)
print('pixels of actual object: ' + str(target_area_pixels))
print('surface area of actual object: ' + str(target_area_actual))

cnts = cv2.drawContours(image, target_cont, -1, (255, 0, 0), 3)

cv2.imshow('Contours', cnts)


cv2.waitKey(0)
cv2.destroyAllWindows