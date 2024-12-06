from src.project_types import UserData, Pixel, ImageCoordsAlias
from src.config import discarded_iteration_number, start_point,affine_transformations_num,symmetry_axes_count,gamma_coeff

from src.core.utils import select_random_element_with_probabilities
from src.core.transformations import generate_valid_affine_transformation,generate_probabilities, apply_variations
from src.core.symmetry import apply_symmetry

from src.visualization.image_renderer import create_fractal_image
from src.visualization.gamma_correction import gamma_correction
from src.visualization.scaling import scale_to_image_coordinates
from src.core.creating_pixel import create_pixel

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
        pixels:dict[ImageCoordsAlias, Pixel]=dict()
        x_cur, y_cur =  start_point[0], start_point[1]

        # Первые discarded_iteration_number итераций не применяем вариации и не создаем пиксели
        for iter in range(-discarded_iteration_number,self.user_data.iterations_number):
            
            affine_transf = select_random_element_with_probabilities(self.affine_transformations,self.affine_probabilities)
            x_cur, y_cur = affine_transf.apply_affine_transformation(x_cur, y_cur)
            
            if iter>0:
                x_cur, y_cur = apply_variations( self.user_data.transformer_function_set,x_cur,y_cur )
                points = apply_symmetry(x_cur, y_cur,symmetry_axes_count)
                 
                for x, y in points:
                    image_x, image_y = scale_to_image_coordinates(
                        x, y,
                        self.user_data.img_width_in_pixels,
                        self.user_data.img_height_in_pixels
                    )
                    create_pixel(pixels, affine_transf, image_x, image_y)

        gamma_correction(pixels,gamma_coeff)
        create_fractal_image(self.user_data.img_width_in_pixels,self.user_data.img_height_in_pixels,pixels)

