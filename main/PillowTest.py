from PIL import Image
from math import floor

img = Image.new("RGB", (100, 100), color="white")
img.format = "PNG"

pixels = img.load()

for i in range(img.size[0]):
    for j in range(img.size[1]):
        if floor(i / 10) % 2 == floor(j / 10) % 2:
            pixels[i, j] = (100, 0, 0)

img.show()
