import cv2
import numpy as np
import imutils




#-------------------------Function------------------------------------------------------
def sliding_window(image, stepSize, windowSize):
 	# slide a window across the image
 	for y in range(0, image.shape[0], stepSize):
         for x in range(0, image.shape[1], stepSize):
 			# yield the current window
             yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
#-------------------------------------------------------------------------------        

winW, winH = (256,256) 
for (x, y, window) in sliding_window(img, stepSize=64, windowSize=(winW, winH)):
    if window.shape[0] != winH or window.shape[1] != winW:
        continue
    clone = img.copy()
    
    cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
    roi = img[y: y+winH, x:x + winW ]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    #cropped = cv2.medianBlur(roi.copy(), 3)
    #cropped = cv2.GaussianBlur(original[y: y+winH, x:x + winW ], (3,3),0)
    #cropped = cv2.fastNlMeansDenoising(original[y: y+winH, x:x + winW ],None,10,7,21)
    roi = cv2.GaussianBlur(roi, (3,3),0)
    #_, roi = cv2.threshold(roi.copy(), 0,255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    roi = cv2.adaptiveThreshold(roi.copy(), 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                    cv2.THRESH_BINARY_INV, 111,39)
    
    
    original[y: y+winH, x:x + winW ] = cv2.cvtColor(roi,cv2.COLOR_GRAY2BGR)
    
    cv2.imshow("cloned", clone)
    cv2.imshow("roi", roi)
    #cv2.imshow("cropped", roi)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    #time.sleep(0.025)

cv2.destroyAllWindows()
