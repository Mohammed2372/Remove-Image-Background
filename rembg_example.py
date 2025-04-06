from rembg import remove
from PIL import Image

input_path = '7fca11681f06985ed77dd2708c8709ae.jpg'
output_path = 'output_image.png'
inp = Image.open(input_path)
out = remove(inp)
out.save(output_path)
Image.open(output_path).show()