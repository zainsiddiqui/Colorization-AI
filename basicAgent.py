import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt
from PIL import Image

def crop_half(image):
  # Splitting image into halves
  a = []
  height, width = image.shape[:2]
  start_row, start_col = int(0), int(0)
  end_row, end_col = int(height ), int(width * .5)
  cropped_top = image[start_row:end_row , start_col:end_col]
  a.append(start_row)
  a.append(end_row)
  a.append(start_col)
  a.append(end_col)
  # print (start_row, end_row) 
  # print (start_col, end_col)

  # cv2.imshow("Cropped Left", cropped_top) 
  # cv2.waitKey(0) 
  # cv2.destroyAllWindows()

  # Let's get the starting pixel coordiantes (top left of cropped bottom)
  start_row, start_col = int(0), int(width* .5)
  # Let's get the ending pixel coordinates (bottom right of cropped bottom)
  end_row, end_col = int(height), int(width)
  cropped_bot = image[start_row:end_row , start_col:end_col]
  a.append(start_row)
  a.append(end_row)
  a.append(start_col)
  a.append(end_col)
  # print (start_row, end_row) 
  # print (start_col, end_col)

  # cv2.imshow("Cropped Right", cropped_bot) 
  # cv2.waitKey(0) 
  # cv2.destroyAllWindows()
  return a

# img = training & testing data
def BasicAgent(img):
  vectorized = img.reshape((-1,3))
  vectorized = np.float32(vectorized)

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  K = 30
  attempts=10
  # Running k means, with k = 5
  ret,label,center=cv2.kmeans(vectorized,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
  center = np.uint8(center)
  res = center[label.flatten()]

  # Array of 5 representative RGB Values
  repColors = center
  print(repColors)

  # Applying filters
  result_image = res.reshape((img.shape))

  # Displaying image
  figure_size = 30
  plt.figure(figsize=(figure_size/2,figure_size/2))
  plt.subplot(1,2,1),plt.imshow(img)
  plt.title('Original Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(1,2,2),plt.imshow(result_image)
  plt.title('Basic Agent Image' ), plt.xticks([]), plt.yticks([])
  plt.show()



# Loading image
original_image = cv2.imread("beach.jpg")

orig=cv2.cvtColor(original_image,cv2.COLOR_BGR2RGB)

# Cropping original image
coord = crop_half(orig)
start_row = coord[0]
end_row = coord[1]
start_col = coord[2]
end_col = coord[3]

imgO = original_image[start_row:end_row , start_col:end_col]
# Obtaining training image
img = orig[start_row:end_row , start_col:end_col]

# Obtaining testing image
greyimg = orig[coord[4]:coord[5] , coord[6]:coord[7]]
greyimg = cv2.cvtColor(greyimg, cv2.COLOR_BGR2GRAY)
# Adding 3-D for combining with colored image
greyimg = cv2.cvtColor(greyimg,cv2.COLOR_GRAY2BGR)

# Images array containing training and testing data
imgs = [imgO,greyimg]
cv2.imshow("grey img", greyimg) 

# height, width,z = img.shape[:3]
# print(height,width,z)
# height, width,z = greyimg.shape[:3]
# print(height,width,z)

# Finding mininmum size
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
# Combining training and testing data
imgs_comb = np.hstack( (np.asarray( imgs ) ))
cv2.imshow("training and testing combined image", imgs_comb) 

# Running basic agent on testing and training data
BasicAgent(orig)
