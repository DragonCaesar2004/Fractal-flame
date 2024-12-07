from src.core.creating_pixel import create_pixel  
from src.project_types import AffineTransformation

 
def test_create_new_pixel():
    pixels = {}
    affine_transf = AffineTransformation(a=0.5,b=0.5,c=0.5,d=0.5,e=0.5,f=0.5,red=10, green=20, blue=30)
    image_x, image_y = 100, 200

    create_pixel(pixels, affine_transf, image_x, image_y)

    assert (image_x, image_y) in pixels
    assert pixels[(image_x, image_y)].red == 10
    assert pixels[(image_x, image_y)].green == 20
    assert pixels[(image_x, image_y)].blue == 30
    assert pixels[(image_x, image_y)].counter == 1

def test_create_pixel_existing_pixel():
    pixels = {}
    affine_transf_1 = AffineTransformation(a=0.5,b=0.5,c=0.5,d=0.5,e=0.5,f=0.5,red=10, green=20, blue=30)
    affine_transf_2 = AffineTransformation(a=0.5,b=0.5,c=0.5,d=0.5,e=0.5,f=0.5,red=90, green=80, blue=70)
    image_x, image_y = 100, 200

    create_pixel(pixels, affine_transf_1, image_x, image_y)
    create_pixel(pixels, affine_transf_2, image_x, image_y)

    assert (image_x, image_y) in pixels
    assert pixels[(image_x, image_y)].red == 50
    assert pixels[(image_x, image_y)].green == 50
    assert pixels[(image_x, image_y)].blue == 50
    assert pixels[(image_x, image_y)].counter == 2  # Было 1, стало 2
