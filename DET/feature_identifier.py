import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

def filterKp(point):
    if point.size > 50:
        return True
    return False

def rotateImage(img, angle, image_centre):
    rows,cols = img.shape
    #print str(cols) + " - " + str(rows)
    M = cv2.getRotationMatrix2D(image_centre,angle + 90,1)
    result = cv2.warpAffine(img,M,(cols,rows))
    return result


def generateFeatureImage(input_path, output_path, file):

    print input_path + " - " + output_path + " - " + file

    file_split = os.path.splitext(os.path.basename(file))
    name = file_split[0]
    ext = file_split[1][1:]

    if ext == 'gif':
        print "***** GIFS ARE NOT SUPPORTED! Need to save do something, else ignore **** " #TODO
        return []
    
    img = cv2.imread(input_path + name+'.'+ext,0)

    # TODO: Maybe resize all images to a typical file resolution first? May help, other threshold will vary for different sizes of the same image

    surf = cv2.SURF(400)
    kp, des = surf.detectAndCompute(img,None)
    #print len(kp)
    #print surf.hessianThreshold
    surf.hessianThreshold = 7000
    kp, des = surf.detectAndCompute(img,None)

    kp = filter(filterKp, kp)

    generated_feature_files = []

    for i, point, in enumerate(kp):
        #print str(i) + " > " + str(point.angle) + "* - " + str(point.class_id) + " - " + str(point.octave) + " - " + str(point.pt) + " - " + str(point.size)
        rotated = rotateImage(img, point.angle, point.pt)
        minx = int(point.pt[0] - point.size/2)
        miny = int(point.pt[1] - point.size/2)
        maxx = int(point.pt[0] + point.size/2)
        maxy = int(point.pt[1] + point.size/2)
        #print "   " + str(minx) + " , " + str(miny) + " - " + str(maxx) + " , " + str(maxy)
        #cv2.rectangle(rotated,(minx,miny),(maxx,maxy),(0,255,0),3)
        cropped = rotated[miny:maxy, minx:maxx]
        outname = output_path + name+'_feature_'+str(i)+'.'+ext
        cv2.imwrite(outname,cropped)
        generated_feature_files.append(outname)

    
    #img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)
    #cv2.imwrite(output_path + name+'_features_surf.'+ext,img2)
    print "      Generated " + str(len(kp)) + " features"
    return generated_feature_files