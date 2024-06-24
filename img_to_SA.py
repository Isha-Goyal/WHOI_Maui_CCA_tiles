
from rembg import remove 
from PIL import Image 
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import numpy as np
import os
import csv

# Iterate through images in folder
directory = '/home/igoyal/WHOI/Maui CCA tile Surface Area/CCA tile photos Exp 2 PDAM'

with open('exp_2_surface_area.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file)

    parent_list = os.listdir(directory)
    parent_list.sort()

    for filename in parent_list:
        f = os.path.join(directory, filename)
    
        # Input and output paths for background removal 
        im_path = f
        output_path = os.path.join(directory, 'temp_no_bkgd.png') 
        
        input = Image.open(im_path)
        
        # Removing the background and turning it to green
        output = remove(input,bgcolor=[0,255,0, 255])

        #Saving the image in the given path 
        output.save(output_path) # note that this is storing to a file that will be overwritten by the next file

        # read and format image to get edges
        image = cv2.imread(output_path)
        image = cv2.resize(image, (0, 0), fx = 0.3, fy = 0.3)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 1, 200)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # Find all contours in image
        contours, hierarchy = cv2.findContours(edged,  
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        
        # Sort the contours from rightmost to leftmost
        contours = sorted(contours, key=lambda c: c[0][0][0], reverse=True)

        # Additional possible displays
        # cv2.imshow('gray', gray) # display grayscale image
        # print("Number of Contours found = " + str(len(contours)))
        # cv2.imshow('Canny Edges After Contouring', edged)  

        # Pulls out the contours that are large enough
        big = [] # stores contours that are large enough
        count = 0

        for i,c in enumerate(contours):
            if cv2.contourArea(c) > 1000: # note, might have to adjust this setup at the beginning to make sure you're getting two
                count+=1
                big.append(i)


        # Find and assume rightmost contour in image is reference (should be a circle of known size)
        ref_cont = contours[big[0]] # note: change this line if the relative position of the reference within the image changes
        ref_area_pixels = cv2.contourArea(ref_cont)
        ref_diam_actual = 0.75 # diameter of penny in inches
        ref_area_actual = np.pi * np.square(ref_diam_actual/2)

        ratio = ref_area_actual/ref_area_pixels # conversion factor of pixels to actual size

        cnts = cv2.drawContours(image, ref_cont, -1, (0,0,255), 2)


        # Find and assume center contour is target
        target_cont = contours[big[1]]
        target_area_pixels = cv2.contourArea(target_cont)
        target_area_actual = target_area_pixels * ratio

        print('surface area of actual object: ' + str(target_area_actual))

        # cnts = cv2.drawContours(image, target_cont, -1, (255, 0, 0), 2)
        # cv2.imshow('Contours', cnts)

        # Remove .jpg from file name and write the surface area to csv
        csvwriter.writerow([filename[0:-4], target_area_actual])

        cv2.destroyAllWindows