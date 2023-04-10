from PIL import Image # pip install Pillow
import sys
import os
import glob
from PIL import ImageOps
import numpy as np

try:
    # console'dan gelen path bilgisini al
    dirPath = sys.argv[1]

    # console'dan gelen size bilgisini al ve tuple[int, int]'e donustur
    backgroundSize = sys.argv[2]
    backgroundSize = backgroundSize.split('x')
    backgroundSize = tuple(map(lambda x : int(x), backgroundSize))

    # console'dan gelen padding bilgisini al
    padding = int(sys.argv[3])

    # console'dan gelen extension listesini al
    imageExtensions = sys.argv[4:]
except :
    # console'da script'in kullanimi hakkinda bilgi ver
    print("Usage: python main.py directoryPath dimension padding ext1 ext2 ext3 ... extN")
    print(r"directoryPath(e.g.): C:\Users\username\Documents\images")
    print(r"dimension(e.g.): 400x400")
    print(r"padding(e.g.): 256")
    print(r"ext1 ext2 ext3 ... extN(e.g.): png jpg webp ...")
    sys.exit(1)

# belirtilen path yoksa hata yazdirip programi sonlandir
if not os.path.exists(dirPath):
    print('The path could not be found')
    sys.exit(1)

# belirtilen path'deki, belirtilen extension'a sahip resimlerin path'lerini al
imagePaths = []
for extension in imageExtensions:
    imagePaths.extend(glob.glob(dirPath + "/*.{ext}".format(ext=extension)))

for imagePath in imagePaths:
    # path'i alinan resmi ac
    image = Image.open(imagePath)
    image.load()

    # resmin boyutlarini belirle
    imageSize = image.size

    # resmin yapistirilacagi beyaz arkaplani olustur
    whiteBackground = Image.new(mode="RGB", 
                                size=backgroundSize, 
                                color='#fff')
    
    # resmi bir kutuya alacak sekilde beyazliklari kirp
    invert_im = image.convert('RGB')
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()
    imageBox = tuple(np.asarray(imageBox))
    croppedImage = image.crop(imageBox)

    # kirpilan resmin boyutlarini belirle
    croppedImageSize = croppedImage.size
    
    # resmi yeniden boyutlandirmak icin boyutlarini belirle
    thumbnailWidth = backgroundSize[0] - padding
    thumbnailHeight = backgroundSize[1] - padding
    thumbnailSize = (thumbnailWidth, thumbnailHeight)

    # resmi yeniden boyutlandir
    croppedImage.thumbnail(thumbnailSize)

    # resmin yapistirilacagi offset'i belirle (arkaplanin ortasina)
    offsetX = (backgroundSize[0] - croppedImage.size[0]) // 2 
    offsetY = (backgroundSize[1] - croppedImage.size[1]) // 2
    offset = (offsetX, offsetY)

    # resmi, belirtilen offset'e yapistir
    whiteBackground.paste(croppedImage, offset)

    # yeni resim adi uret
    label = 'resized'
    imagePathWithoutExtension, imageExtension = imagePath.rsplit('.', 1)
    generatedImagePath = '{path}-{label}.{extension}'.format(path=imagePathWithoutExtension, 
                                                             label=label, 
                                                             extension=imageExtension)

    # uretilen isimle resmi kaydet
    whiteBackground.save(generatedImagePath)