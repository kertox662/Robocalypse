from pyscreenshot import grab
from PIL import Image, ImageFilter

im = grab(bbox=(20, 50, 300, 400))
im = im.filter(ImageFilter.BLUR)

im.show()
