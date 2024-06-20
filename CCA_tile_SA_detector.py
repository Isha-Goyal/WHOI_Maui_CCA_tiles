from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import numpy as np

im_path = '/home/igoyal/WHOI/tile_images/red_reg_1_back.jpg'
image = cv2.imread(im_path)
image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)
# image = cv2.resize(image, (768, 1024)) #resize image to fit in window --> note: adjust later to fit properly/adjust automatically

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 100, 200)

edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)


contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

cv2.imshow('window_name', image)
# cv2.imshow('gray', gray)

print("Number of Contours found = " + str(len(contours)))
cv2.imshow('Canny Edges After Contouring', edged)  

big = np.array([])
count = 0

for i,c in enumerate(contours):
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) > 10000:
		count+=1
		img = cv2.drawContours(image, c, -1, (0, 255, 0), 3)
		# big = np.append(big, c)
		
print(count)
# conts = [contours[i] for i in big]

# areas = cv2.drawContours(image, big, -1, (0, 255, 0), 3)
cv2.imshow('Large Area Edges', img) 
    

# find and assume bottom-most contour in image is reference (should be a circle of known size)
ref_cont = contours[0]
ref_area_pixels = cv2.contourArea(ref_cont)
ref_diam_actual = 1.25 # actual diameter of your reference object (in whatever units)
ref_area_actual = np.pi * np.square(ref_diam_actual/2)
# ref_dia_pixels = np.sqrt(ref_area/np.pi) * 2
# ref_dia_actual = 20 # actual measurement of physical circular object's diameter
ratio = ref_area_actual/ref_area_pixels

cnt = contours[0]
cnts = cv2.drawContours(image, ref_cont, -1, (0,255,0), 3)


# print(ref_dia_pixels)
# print(ref_dia_actual)
print('area of reference object: ' + str(ref_area_actual))
print('ratio: ' + str(ratio))

# find rect contour and say size
target_cont = contours[1]
target_area_pixels = cv2.contourArea(target_cont)
target_area_actual = target_area_pixels * ratio
# print(target_cont)
print('surface area of actual object: ' + str(target_area_actual))

cnts = cv2.drawContours(image, target_cont, -1, (255, 0, 0), 3)

cv2.imshow('Contours', cnts)

# leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
# rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
# topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
# bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

# image = cv2.circle(image, leftmost, radius=5, color=(0, 0, 0), thickness=-1)
# image = cv2.circle(image, rightmost, radius=5, color=(0, 0, 0), thickness=-1)
# image = cv2.circle(image, topmost, radius=5, color=(0, 0, 0), thickness=-1)
# image = cv2.circle(image, bottommost, radius=5, color=(0, 0, 0), thickness=-1)
# cv2.imshow('contour points', image)

cv2.waitKey(0)
cv2.destroyAllWindows