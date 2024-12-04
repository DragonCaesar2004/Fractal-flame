
from src.project_types import UserData, FractalLimits, PointAlias
from src.config import discarded_iteration_number, start_point,affine_transformations_num
from src.core.transformations import generate_valid_affine_transformation,generate_probabilities, apply_variations
from src.visualization.points_to_pixels_converting import convert_points_to_pixels
from src.core.utils import select_random_element_with_probabilities
from src.visualization.image_renderer import create_fractal_image


class Manager:

    def __init__(self, user_data: UserData):

        self.user_data = user_data
        # Генерация коэффициентов для всех преобразований
        self.affine_transformations = [
            generate_valid_affine_transformation() for _ in range(affine_transformations_num)
        ]
        #  Генерация вероятностей для аффинных преобразований
        self.affine_probabilities = generate_probabilities(affine_transformations_num)

        
    def create_fractal_flame(self, multistream:bool = False)-> None:
        points: set[PointAlias]=set()
        fractal_limits = FractalLimits()
        x_cur, y_cur =  start_point[0], start_point[1]
        
        for iter in range(-discarded_iteration_number,self.user_data.iterations_number):
            
            affine_transf = select_random_element_with_probabilities(self.affine_transformations,self.affine_probabilities)
            x_cur, y_cur = affine_transf.apply_affine_transformation(x_cur, y_cur)
            
            if iter>0:

                x_cur, y_cur = apply_variations( self.user_data.transformer_function_set,x_cur,y_cur )
                fractal_limits.update(x_cur, y_cur)
                points.add((x_cur, y_cur,affine_transf.red,affine_transf.green,affine_transf.blue))
        # сразу в цикле не конвертирую точки в пиксели, 
        # так как сначала надо узнать максимальные и минимальные значения координат 

        pixels =  convert_points_to_pixels(points,self.user_data.img_width_in_pixels,self.user_data.img_height_in_pixels,fractal_limits)
        create_fractal_image(self.user_data.img_width_in_pixels,self.user_data.img_height_in_pixels,pixels)

        



