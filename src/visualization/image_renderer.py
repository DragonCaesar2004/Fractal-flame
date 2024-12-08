from PIL import Image

from src.project_types import ImageCoordsAlias, Pixel


def create_fractal_image(
    img_width_in_pixels: int,
    img_height_in_pixels: int,
    pixels: dict[ImageCoordsAlias, Pixel],
    output_path: str = "fractal_flame.png",
) -> None:
    """
    Создает изображение фрактала на основе заданных пикселей и сохраняет его в файл.

    Эта функция создает новое RGB изображение заданной ширины и высоты,
    заполняет его пикселями на основе их координат и сохраняет результат
    в указанный файл.
    """
    img = Image.new("RGB", (img_width_in_pixels, img_height_in_pixels), "black")
    for image_coords, pixel in pixels.items():
        image_x, image_y = image_coords
        red, green, blue = pixel.red, pixel.green, pixel.blue
        if 0 <= image_x < img_width_in_pixels and 0 <= image_y < img_height_in_pixels:
            img.putpixel((image_x, image_y), (red, green, blue))

    img.save(output_path)
