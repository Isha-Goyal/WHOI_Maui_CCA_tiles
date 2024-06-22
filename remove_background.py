
# Importing Required Modules 
from rembg import remove 
from PIL import Image 
  
# Store path of the image in the variable input_path 
input_path =  '/home/igoyal/WHOI/WHOI_Maui_CCA_tiles/maui CCA tile photos/P6210549.JPG' 
  
# Store path of the output image in the variable output_path 
output_path = '/home/igoyal/WHOI/WHOI_Maui_CCA_tiles/test_no_bkgd.png' 
  
# Processing the image 
input = Image.open(input_path) 
input.show()
  
# Removing the background from the given Image 
output = remove(input,bgcolor=[0,255,0, 255])
# output = remove(input) 
output.show()
  
#Saving the image in the given path 
output.save(output_path) 
