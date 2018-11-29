
# =============================================================================
# Custom ImageData Generation
# 1. Needs folder structure in source folder. 
# 
#   TrainData
#     ├── Category_1
#     │        ├── image1
#     │        ├──image1
#     └── Category_2
#             ├── image1
#             ├──image1
# 
# 2. Just provide the source and destination folders for creating the Data 
# 3. Run the script
# =============================================================================


import keras
import cv2, numpy as np, os
from keras.preprocessing.image import ImageDataGenerator
import shutil


class ImageGeneration():
    
    def __init__(self, srcDir, dstDir, noOfImagesToGenerate = 10000):
        
        self.path = os.path.dirname(os.path.abspath('__file__')) + '/'
        self.maxCount = noOfImagesToGenerate
        self.srcDir = srcDir
        self.dstDir = dstDir
        self.dataGen = ImageDataGenerator(shear_range = 0.15, 
                    zoom_range = 0.05,
                    rotation_range=0.2,
                    width_shift_range=0.1,
                    height_shift_range=0.1,
                    horizontal_flip=True)
        
        self.dataGenNoise = ImageDataGenerator(shear_range = 0.15, 
                    zoom_range = 0.05,
                    rotation_range=0.2,
                    width_shift_range=0.1,
                    height_shift_range=0.1,
                    horizontal_flip=True,
                    preprocessing_function= self.addGaussNoise)

        
        
        
    #function for adding noise into the image    
    def addNoise(self,x_batch):
        noise_factor = 0.1
        x_batch = x_batch + noise_factor * np.random.normal(loc=0,scale=1,size=x_batch.shape)
        x_batch = np.clip(x_batch, 0.0, 1.0)
        return x_batch
    
    def addGaussNoise(self, image):
        amount = 0.03
        out = np.copy(image)
        num_pepper = np.ceil(amount* image.size * (1. - 0.5))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0
        return out
    # =============================================================================
    #     row,col,ch= image.shape
    #     mean = 0
    #     var = 0.1
    #     sigma = var**0.5
    #     gauss = np.random.normal(mean,sigma,(row,col,ch))
    #     gauss = gauss.reshape(row,col,ch)
    #     noisy = image + gauss
    #     return noisy
    # =============================================================================

    def processImages(self):
        #getting all the directories from the parent folder.
        _dir = [item for item in os.listdir(self.srcDir) if '.DS_Store' not in item]
        
        #gettign the info about the file count per directory : required if you have reference for image generation
        # =============================================================================
        # maxCount = np.max([len(os.listdir(srcDir + folder)) for folder in _dir ])
        # print('Maximum count found is :',  maxCount)
        # 
        # =============================================================================
        #generating 30000 images from avaliable images
        #self.maxCount = 30000
        
        for folder in _dir:
            print('Starting folder', folder)
            print('Moving this folder to new destination for image data generation')
            shutil.move(self.srcDir+ folder, self.dstDir )
            print('Folder Moved')
            #Creating object of Image Generator
            imageGenerator = self.dataGen.flow_from_directory( self.dstDir ,
                                                    target_size = (300,300),
                                                    class_mode = 'categorical',
                                                    batch_size = 500,
                                                    color_mode='rgb',
                                                    shuffle=True,
                                                    seed=88,
                                                    save_to_dir= self.dstDir,
                                                    save_prefix = '@_')
        
            imageGeneratorNoise =self.dataGenNoise.flow_from_directory( self.dstDir ,
                                                    target_size = (300,300),
                                                    class_mode = 'categorical',
                                                    batch_size = 500,
                                                    color_mode='rgb',
                                                    shuffle=True,
                                                    seed=88,
                                                    save_to_dir= self.path +  'Test/',
                                                    save_prefix = '@_Noise_')
        
            #Find out the images in Copied folder
            totalCount = len(os.listdir(self.dstDir + folder))
            numberOfImagesToGenerate = self.maxCount - totalCount
            # Identify the lopping count for data Generation
            loopCount = numberOfImagesToGenerate // 500 # batch Size
        
            print('DataGeneration Started')
            for i in range(0,loopCount):
                if i < 0.8 * loopCount:
                    try:
                        imageGenerator.next()
                    except Exception as e:
                        print('ImageFile is not in proper form: -', e)
                        continue
                else:
                    try:
                        imageGeneratorNoise.next()
                    except Exception as e:
                        print('ImageFile is not in proper form: -', e)
                        continue
            
            print('Data Generated')
            # Moving back the files to Same folder
            srcFiles = [files for files in os.listdir(self.dstDir) if '.png' in files]
            dst = [files for files in os.listdir(self.dstDir) if '.' not in files] 
        
            for file in srcFiles :  
                try:
                    shutil.move(self.dstDir+file, self.dstDir+ dst[0] + '/' )
                except FileExistsError as e:
                    print('File already Exists: ', e)
                    shutil.rmtree(self.dstDir+ dst[0] + '/' + file)
                    shutil.move(self.dstDir+file, self.dstDir+ dst[0] + '/' )
                    #continue
            print('Files moved back to folder {} successfully and it has file counts {}'.format(dst[0],
                  len(os.listdir(self.dstDir+ dst[0]) )))
        
            #Now moving the Entire folder back to its original place
            
            shutil.move(self.dstDir + folder, self.srcDir )
            
            print('Tadda......Folder Moved.. Going for Next Folder')




'''Testing code'''

path = os.path.dirname(os.path.abspath('__file__')) + '/'
srcDir = path + 'FashionData/Train_Directory/'
dstDir = path + 'Test/'

obj = ImageGeneration(srcDir, dstDir, noOfImagesToGenerate= 25000)

obj.processImages()