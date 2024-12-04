from src.visualization.scaling import scale_to_image_coordinates    
from src.project_types import FractalLimits,Pixel, ImageCoordsAlias, PointAlias

def convert_points_to_pixels(points: set[PointAlias],img_width_in_pixels:int ,img_height_in_pixels:int,fractal_limits:FractalLimits ) -> dict[ImageCoordsAlias, Pixel]:
    pixels:dict[ImageCoordsAlias, Pixel]=dict()
    for coord_x, coord_y,red, green, blue in points:
        image_x, image_y =scale_to_image_coordinates(coord_x, coord_y,img_width_in_pixels,img_height_in_pixels,fractal_limits)
        if (image_x, image_y) in pixels:
            pixels[(image_x, image_y)].update_color(red, green, blue )
        else:
            pixels[(image_x, image_y)]=Pixel(red=red, green=green, blue=blue)
        pixels[(image_x, image_y)].increment_counter()
    return pixels