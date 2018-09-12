# =============================================================================
# Class for Creating Images for training with shape 32 by 32
# =============================================================================
class ImageSetup():
    def __init__(self, srcPath, dstPath):
        self.srcPath = srcPath
        self.dtPath = dstPath


    def CreateImages(self):
        folders = [i for i in os.listdir(self.srcPath) if '.DS_Store' not in i]
        
        for folder in folders:
            print('Starting folder ', folder)
            images = [items for items in os.listdir(self.srcPath + folder) if '.DS_Store' not in items]
            for img in images:
                print('Starting Image ', self.srcPath + folder + '/' + img)
                '''loading the Image
            blurring the image
            Threshholding it 
            get the contour 
            resizing the contour to 32,32 
            Saving it with same name in same folder
            '''
                image = cv2.imread(self.srcPath + folder +'/' + img)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                image = cv2.GaussianBlur(image,(3,3),0)
                _,thresh = cv2.threshold(image.copy(),0, 255, cv2.THRESH_OTSU |cv2.THRESH_BINARY)
                
                _,contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                
                print(len(contours))
                cnt = contours[0]
                #getting the boundinx box of the contour
                x,y,w,h = cv2.boundingRect(cnt)
                
                cropped_image = image[y:y+h,x:x+w]
                print('shape of croped iamges is ', cropped_image.shape)
                cropped_image = cv2.resize(cropped_image, (32,32), cv2.INTER_AREA)
                print('shape of  Resized croped images is ', cropped_image.shape)
                
                #wrting the image to folder
                cv2.imwrite(self.srcPath + folder +'/' + img, cropped_image)
                #break
            print('Done with Folder ', folder)
            #break
            
# Creating the Object of the class and calling the Method            
            
obj = ImageSetup(srcPath='/Users/vk250027/Documents/Bevmo/DATA_ver1/Train/',dstPath=None)
         
obj.CreateImages()                
                
