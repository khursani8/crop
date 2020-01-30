import xml.etree.ElementTree
import os
import cv2
import random
import string
import errno
from PIL import Image
import numpy as np
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path

from util import *

#calling function to scan the folder and , set variable filesimg to ret_list of the folder, print length of files(.JPG , .jpg) in the folder
#############################jangan kacau
src_dirimgxml=Path('Orig')
dir_save_img=Path("nadi2try")
filesimg=filelistimg(src_dirimgxml)
print(len(filesimg))

#check if the image file has corresponding xml file and the file is accessible properly
#############################jangan kacau
for nameimg in filesimg:
    
    xml_nameimg = os.path.join(src_dirimgxml,os.path.basename(nameimg).rsplit(".")[0]+".xml")
    
    if os.path.isfile(xml_nameimg) and os.access(xml_nameimg, os.R_OK):
        print (" xml File of the image exists and is readable")
    else:
        print ("Either the file is missing or not readable")    
        os.remove(nameimg)
#############################jangan kacau

if not os.path.exists(dir_save_img):
    try:
        os.makedirs(dir_save_img)
    except OSError as error:
        if error.errno != errno.EEXIST:
         raise

xml_list=filelistxml(src_dirimgxml)
print(len(xml_list))

for entry in xml_list:
    file_xml=xml.etree.ElementTree.parse(entry).getroot()
    paddy_bboxes = []

    for haha in file_xml:
        if haha.tag=="object":
            print("this is an object")
            objects = file_xml.find("object")
            for item in objects:
                if item.tag == "bndbox":
                    print (item.tag)
                    xmin,ymin,xmax,ymax = get_voc_coord(item)
                    paddy_bboxes.append((xmin,ymin,xmax,ymax))
                    print("The coordinates of file "+ entry + " is "+ str(paddy_bboxes))
                    img = get_img(src_dirimgxml,entry)
                    if img is None:
                        continue
                    #copy image for drawing bboxes
                    write_image = img.copy()
                    #change its color scheme because PIL use RGB, while OpenCV use BGR
                    write_image = cv2.cvtColor(write_image, cv2.COLOR_BGR2RGB)
                    #convert image from opencv to PIL format
                    pil_image = Image.fromarray(write_image)
                    draw = ImageDraw.Draw(pil_image)
                    # draw.line((xmin, ymin, xmin, ymax), fill='yellow', width=3)
                    # draw.line((xmin, ymin, xmax, ymin), fill='yellow', width=3)
                    # draw.line((xmax, ymin, xmax, ymax), fill='yellow', width=3)
                    # draw.line((xmin, ymax, xmax, ymax), fill='yellow', width=3)
                    draw.rectangle([(xmin,ymin),(xmax,ymax)],width=3,outline='yellow')
                    write_image = np.array(pil_image)
                    #change color scheme back
                    write_image = cv2.cvtColor(write_image, cv2.COLOR_RGB2BGR)
                    # h,w,c = img.shape
                    save_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(44))
                    save_image_name = os.path.join(dir_save_img,save_name+".jpg")
                    cv2.imwrite(save_image_name,write_image)