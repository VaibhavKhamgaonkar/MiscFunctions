import cv2, os, time
import numpy as np
from threading import Thread
from multiprocessing import Pool
import shutil
from tqdm import tqdm

import argparse

class TrainTestSplit():
    """ To divide the Data into Train Test from each category"""
    def __init__(self, srcPath, trainSplitFactor = 0.8):
        ''' srcPath is main parent folder path where all the categories are present. '''
        self.srcPath = srcPath + '/'
        self.allCategories = [self.srcPath + item + '/' for item in os.listdir(self.srcPath) 
                                if 'data' not in str(item).lower()]
        self.trainFactor = trainSplitFactor
        
        """ check whether Training and Testing Folder Exist of not """
        if not os.path.isdir(self.srcPath + 'TrainData'):
            os.makedirs(self.srcPath + 'TrainData')
        
        if not os.path.isdir(self.srcPath + 'ValidationData'):
            os.makedirs(self.srcPath + 'ValidationData')
    
    
    def TrainTestSplit(self,catFolder):
        #print(catFolder)
        """ CatFolder is the folder associated with each category """
        allImages = os.listdir(catFolder)
        #suffling all the images
        np.random.shuffle(allImages)
        """ get the Count of images in the Category folder """
        totalImgCount = len(allImages)
        ''' getting training and Testing Count'''
        trainImages = allImages[0:int(totalImgCount* 0.8)]
        testImages = allImages[int(totalImgCount* 0.8) : ]
        """ GEtting the Actual folder required to be created in training and validation folders """
        cat = str(catFolder).split('/')[-2]
        #print(f'Category is {cat}')
        """ checking whether Category folder Exist in Trainign and validation folder"""
        if not os.path.isdir(self.srcPath + 'TrainData/' + cat):
            os.makedirs(self.srcPath + 'TrainData/' + cat)
            print(f'Folder created in Training set {cat}')
        if not os.path.isdir(self.srcPath + 'ValidationData/' + cat):
            os.makedirs(self.srcPath + 'ValidationData/' + cat)
            print(f'Folder created in validation set {cat}')
        
        """Moving the Training and testing files to respective Folders """
        print('Moving files to respective categories')
        for img in tqdm(trainImages, unit='Images'):
            shutil.move(catFolder + '/' + img, self.srcPath + 'TrainData/' + cat + '/')
        
        for img in tqdm(testImages, unit='Images'):
            shutil.move(catFolder + '/' + img, self.srcPath + 'ValidationData/' + cat + '/')
        
        """ finally deleting the Current Category folder """
        if len(os.listdir(catFolder)) < 1:
            shutil.rmtree(catFolder)
        else:
            print(f"Directory is Not Empty {catFolder}")
        


def main(path):
    
    """ initialising Pool """
    pool = Pool(processes = 3)
    ''' Initialising Classs Object '''    
    obj = TrainTestSplit(srcPath= path, trainSplitFactor= 0.85)
    
    pool.map(obj.TrainTestSplit, obj.allCategories)
    
    

    
if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="path to the Dataset folder")
    args = vars(ap.parse_args())
    
    main(args['path'])
    
    

        