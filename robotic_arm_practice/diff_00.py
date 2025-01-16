from PIL import Image, ImageChops

img1, img2 = Image.open('m_01.jpg'), Image.open('m_02.jpg')

diff = ImageChops.subtract(img1, img2)

if diff.getbbox():
    diff.show()
else:
    print("NO DIFF")