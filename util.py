import os
import cv2

#declaring function and its definition
#############################jangan kacau
def filelistimg(directoryimg):
    ret_list = []
    for folder, subs, files in os.walk(directoryimg):
        for filename in files:
            if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".PNG") or filename.endswith(".png") and not '-back' in filename:
                ret_list.append(os.path.join(directoryimg,filename))
    return ret_list
###########################the jangan kacau

#declaration of function and its definition fielistxml. The function loops in the disrectory  scans through the folder to find .xml files 
def filelistxml(directory):
    ret_list = []
    for file in os.listdir(directory):
        if file.endswith(".xml"):
            ret_list.append(os.path.join(directory,file))
    return ret_list

def get_voc_coord(item):
    xmin=int(item.find("xmin").text)
    ymin=int(item.find("ymin").text)
    xmax=int(item.find("xmax").text)
    ymax=int(item.find("ymax").text)
    return xmin,ymin,xmax,ymax

def get_img(src_dirimgxml,entry):
    img_name = os.path.join(src_dirimgxml,os.path.basename(entry).rsplit(".")[0]+".jpg")
    img = cv2.imread(img_name)
    if img is  None:
        print("The format is .jpg")

    if img is None:
        img_name = os.path.join(src_dirimgxml,os.path.basename(entry).rsplit(".")[0]+".png")
        img = cv2.imread(img_name)
        if img is not None:
            print("The format is .png")


    if img is None:
        img_name = os.path.join(src_dirimgxml,os.path.basename(entry).rsplit(".")[0]+".JPG")
        img = cv2.imread(img_name)
        if img is not None:
            print("The format is .JPG")


    if img is None:
        print("File image rosak" + img_name)     
        try:
            print("huhu")
            #os.remove(img_name)
        except FileNotFoundError:
            print("file doesnt exist deleted by previous rules ")
            #os.remove(entry)        
    return img