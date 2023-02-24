from django.core.files.storage import FileSystemStorage
import os



def image_upload(img,img_path):
    fs = FileSystemStorage()
    img_path = img_path+img.name
    file = fs.save(img_path, img)
    return (file)
