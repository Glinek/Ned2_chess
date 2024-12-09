from defisheye import Defisheye

dtype = 'linear'
format = 'fullframe'
fov = 180
pfov = 180
img = r"F:\PjSB1 - Current, Hibernating projects\Current Projects\Niryo chess\development\boardPhotos-mk2\board1.jpg"
img_out = f"a.jpg"

obj = Defisheye(img, dtype=dtype, format=format, fov=fov, pfov=pfov)

# To save image locally 
obj.convert(outfile=img_out)

# To use the converted image in memory

new_image = obj.convert()