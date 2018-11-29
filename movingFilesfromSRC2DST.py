import numpy as np, os,time
#import cv2
import shutil

path = 'path of folder to be moved'

folders = [i for i in os.listdir(path) if '.DS_Store' not in i]

for folder in folders:
    #verify the folder contains another folder ?
    check = [items for items in os.listdir(path + folder) if '.' not in items]
    if len(check) > 0:
        print('Started : ', folder)
        #getting the Data from new folder and restoring it back to its previous folder
        toCopy = os.listdir(path + folder + '/' + check[0])
        #Looping through each file and storing it back to previous folder
        print('started moving files from {}...'.format(check[0]))
        for file in toCopy:
            #print(file)
            #renaming the file
            #file = os.rename(file, '__' + file )
            
            src = path + folder + '/' + check[0] + '/' + file
            dst = path + folder + '/' + '_1_' + file
            try:
                shutil.move(src, dst)
            except:
                print('No file to copy' )
        print('{} folder is empty'.format(check[0]))        
        shutil.rmtree(path + folder + '/' + check[0])
