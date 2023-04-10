from PIL import Image # pip install Pillow
import sys
import glob
from PIL import ImageOps
import numpy as np


# Trim all png images with white background in a folder
# Usage "python PNGWhiteTrim.py ../someFolder padding"



try:
    folderName = sys.argv[1]
    padding = int(sys.argv[2])
    padding = np.asarray([-1*padding, -1*padding, padding, padding])
except :
    print("Usage: python PNGWhiteTrim.py ../someFolder padding")
    sys.exit(1)

filePaths = glob.glob(folderName + "/*.png") +  glob.glob(folderName + "/*.jpg") +  glob.glob(folderName + "/*.webp")#search for all png images in the folder

for filePath in filePaths:
    image=Image.open(filePath)
    image.load()
    imageSize = image.size

    # remove alpha channel
    invert_im = image.convert("RGB")

    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()
    imageBox = tuple(np.asarray(imageBox)+padding)

    cropped=image.crop(imageBox)
    print(filePath, "Size:", imageSize, "New Size:", imageBox)
    cropped.save(filePath)

# def resize(image_pil, width, height):
#     '''
#     Resize PIL image keeping ratio and using white background.
#     '''
#     ratio_w = width / image_pil.width
#     ratio_h = height / image_pil.height
#     if ratio_w < ratio_h:
#         # It must be fixed by width
#         resize_width = width
#         resize_height = round(ratio_w * image_pil.height)
#     else:
#         # Fixed by height
#         resize_width = round(ratio_h * image_pil.width)
#         resize_height = height
#     image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
#     background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
#     offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
#     background.paste(image_resize, offset)
#     return background.convert('RGB')

# def resize(ImageFilePath):

#     from PIL import Image
#     image = Image.open(ImageFilePath, 'r')
#     image_size = image.size
#     width = image_size[0]
#     height = image_size[1]

#     if(width != height):
#         width = 400
#         height = 400

#         ratio_w = width / image.width
#         ratio_h = height / image.height
#         if ratio_w < ratio_h:
#             # It must be fixed by width
#             resize_width = width
#             resize_height = round(ratio_w * image.height)
#         else:
#             # Fixed by height
#             resize_width = round(ratio_h * image.width)
#             resize_height = height
#         image_resize = image.resize((resize_width, resize_height), Image.ANTIALIAS)
#         background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
#         offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
#         background.paste(image, offset)
#         background.save('out.png')
#         print("Image has been resized !")
#     else:
#         print("Image is already a square, it has not been resized !")

# for image in filePaths:
#     resize(image)