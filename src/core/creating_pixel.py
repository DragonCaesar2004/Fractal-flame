from src.project_types import Pixel, ImageCoordsAlias, AffineTransformation


def create_pixel(
    pixels: dict[ImageCoordsAlias, Pixel],
    affine_transf: AffineTransformation,
    image_x: int,
    image_y: int,
) -> None:
    """
    Создает объект типа Pixel, добавляет в словарь pixels,
    если по заданным координатам image_x, image_y нет его нет в pixels.

    Иначе обновляет цвет пикселя. Также в любом случае обновляет счетчик пикселя.
    """

    if (image_x, image_y) in pixels:
        pixels[(image_x, image_y)].update_color(
            affine_transf.red, affine_transf.green, affine_transf.blue
        )
    else:
        pixels[(image_x, image_y)] = Pixel(
            red=affine_transf.red, green=affine_transf.green, blue=affine_transf.blue
        )

    pixels[(image_x, image_y)].increment_counter()


def combine_pixels(
    results: list[dict[ImageCoordsAlias, Pixel]]
) -> dict[ImageCoordsAlias, Pixel]:
    """Объединяет результаты нескольких параллельных задач обработки пикселей в один словарь."""
    combined_pixels: dict[ImageCoordsAlias, Pixel] = {}

    for proc_pixels in results:
        for coord, pixel in proc_pixels.items():
            if coord in combined_pixels:
                combined_pixels[coord].counter += pixel.counter
                combined_pixels[coord].update_color(pixel.red, pixel.green, pixel.blue)

            else:
                combined_pixels[coord] = Pixel(
                    counter=pixel.counter,
                    red=pixel.red,
                    green=pixel.green,
                    blue=pixel.blue,
                )
    return combined_pixels
