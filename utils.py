
import os

images_path = os.path.join(os.getcwd(), 'images')

def get_all_image():

    list_img = os.listdir(images_path)

    images = []

    for _file in list_img:
        if _file.endswith(".jpg") or _file.endswith(".png") or _file.endswith(".jpeg"):
            img_path = os.path.join(images_path, _file)
            images.append(img_path)
    
    return images











