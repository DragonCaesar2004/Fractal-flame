def scale_to_image_coordinates(coord_x:float, coord_y: float, img_width:int, img_height:int,fractal_limits)->tuple[int,int]:
    """
    Преобразует координаты в диапазоне (x_min, x_max, y_min, y_max) в пиксельные координаты.
    """

    # Масштабируем x и y в размеры изображения (с учётом диапазонов)
    image_x = int((coord_x - fractal_limits.x_min) / (fractal_limits.x_max - fractal_limits.x_min) * (img_width - 1))
    image_y = int((coord_y - fractal_limits.y_min) / (fractal_limits.y_max - fractal_limits.y_min) * (img_height - 1))
    
    return image_x, image_y