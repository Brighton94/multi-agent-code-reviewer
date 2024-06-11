import math


def cylinder_area(radius, height):
    """
    Calculate the surface area of a cylinder.

    Parameters:
    radius (float): The radius of the cylinder.
    height (float): The height of the cylinder.

    Returns:
    float: The surface area of the cylinder.
    """
    base_area = math.pi * radius**2
    lateral_area = 2 * math.pi * radius * height
    total_area = 2 * base_area + lateral_area
    return total_area


# Example usage:
radius = 5
height = 10
area = cylinder_area(radius, height)
print(f"The surface area of the cylinder is: {area:.2f}")
