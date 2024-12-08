import math

from src.project_types import PointCoordsAlias


def apply_symmetry(
    x: float, y: float, symmetry_axes_count: int
) -> list[PointCoordsAlias]:
    """Генерируем зеркальные отображения точки относительно симметричных осей."""
    symmetrical_points = [(x, y)]
    # Вычисляем угол поворота в радианах
    angle_step = 2 * math.pi / symmetry_axes_count
    for i in range(1, symmetry_axes_count):
        angle = angle_step * i
        sym_x = x * math.cos(angle) - y * math.sin(angle)
        sym_y = x * math.sin(angle) + y * math.cos(angle)
        symmetrical_points.append((sym_x, sym_y))

    return symmetrical_points
