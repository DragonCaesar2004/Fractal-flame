from PIL import Image
from src.project_types import Pixel,ImageCoordsAlias 

def create_fractal_image(img_width_in_pixels:int,img_height_in_pixels:int, pixels: dict[ImageCoordsAlias, Pixel], output_path: str = 'fractal_flame.png'):
     # Масштабирование и построение пикселей
    img = Image.new('RGB', (img_width_in_pixels, img_height_in_pixels), "black")
    for image_coords  in pixels:
        image_x, image_y = image_coords
        red, green, blue = pixels[image_coords].red, pixels[image_coords].green, pixels[image_coords].blue 
        if 0 <= image_x < img_width_in_pixels and 0 <= image_y < img_height_in_pixels:
            img.putpixel((image_x, image_y), (red, green, blue))
     
    img.save(output_path)


