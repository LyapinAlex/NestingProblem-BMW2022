import math, random
import numpy as np
from typing import List, Tuple

def clip(value, lower, upper):
    """
    Given an interval, values outside the interval are clipped to the interval
    edges.
    """
    return min(upper, max(value, lower))

def random_angle_steps(steps: int, irregularity: float) -> List[float]:
    """Generates the division of a circumference in random angles.

    Args:
        steps (int):
            the number of angles to generate.
        irregularity (float):
            variance of the spacing of the angles between consecutive vertices.
    Returns:
        List[float]: the list of the random angles.
    """
    # generate n angle steps
    angles = []
    lower = (2 * math.pi / steps) - irregularity
    upper = (2 * math.pi / steps) + irregularity
    cumsum = 0
    for i in range(steps):
        angle = random.uniform(lower, upper)
        angles.append(angle)
        cumsum += angle

    # normalize the steps so that point 0 and point n+1 are the same
    cumsum /= (2 * math.pi)
    for i in range(steps):
        angles[i] /= cumsum
    return angles

def generate_polygon(center: Tuple[float, float], avg_radius: float,
                     irregularity: float, spikiness: float,
                     num_vertices: int) -> List[Tuple[float, float]]:
    """
    Start with the center of the polygon at center, then creates the
    polygon by sampling points on a circle around the center.
    Random noise is added by varying the angular spacing between
    sequential points, and by varying the radial distance of each
    point from the centre.

    Args:
        center (Tuple[float, float]):
            a pair representing the center of the circumference used
            to generate the polygon.
        avg_radius (float):
            the average radius (distance of each generated vertex to
            the center of the circumference) used to generate points
            with a normal distribution.
        irregularity (float):
            variance of the spacing of the angles between consecutive
            vertices.
        spikiness (float):
            variance of the distance of each vertex to the center of
            the circumference.
        num_vertices (int):
            the number of vertices of the polygon.
    Returns:
        np.array[Tuple[float, float]]: list of vertices, in CCW order.
    """
    # Parameter check
    if irregularity < 0 or irregularity > 1:
        raise ValueError("Irregularity must be between 0 and 1.")
    if spikiness < 0 or spikiness > 1:
        raise ValueError("Spikiness must be between 0 and 1.")

    irregularity *= 2 * math.pi / num_vertices
    spikiness *= avg_radius
    angle_steps = random_angle_steps(num_vertices, irregularity)

    # now generate the points
    points = np.empty((num_vertices, 2))
    angle = random.uniform(0, 2 * math.pi)
    for i in range(num_vertices):
        radius = clip(random.gauss(avg_radius, spikiness), 0, 2 * avg_radius)
        # point = (center[0] + radius * math.cos(angle),
        #          center[1] + radius * math.sin(angle))
        points[i] = [center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)]
        angle += angle_steps[i]

    return points

def create_size(radius):
    size = random.uniform(0,100)
    if size<75:
        avg_radius = random.uniform(radius / 27, radius / 15)
    elif size<96:
        avg_radius = random.uniform(radius / 9.5, radius / 8)
    elif size<100:
        avg_radius = random.uniform(radius / 6.6, radius / 5.5)
    return avg_radius*1.8

def x_axis_compression(polygon):
    compression_ratio = 0.25
    ratio = random.uniform(1-compression_ratio, 1+compression_ratio)
    for point in polygon:
        point[0]*=ratio
    return polygon

def random_polygons(num_polygons, max_polygon_size, min_num_vertices = 6, max_num_vertices = 20, irregularity=0.05, spikiness=0.3):
    """
    irregularity - отвечает за откланение между вершинами, принимает значения от 0 до 1;\\
    spikiness - отвечает за вогнутость/выпуклось вершин, принимает значения от 0 до 1;\\
    Чтобы предметы гарантированно влезали max_polygon_size делать меньше, чем ... [читать полностью]
    """
    polygons = np.full(num_polygons, None)
    for i in range(num_polygons):
        num_vert = random.randint(min_num_vertices, max_num_vertices)
        polygon = generate_polygon(
            center=(max_polygon_size, max_polygon_size),
            avg_radius=create_size(max_polygon_size),
            irregularity = irregularity,
            spikiness = spikiness,
            num_vertices=num_vert)
        x_axis_compression(polygon)

        polygons[i] = polygon
    return polygons

def draw_polygon(points) -> None:
    from matplotlib import pyplot as plt
    from matplotlib import patches
    fig, ax = plt.subplots()

    MAX_SIZE_LIM = np.amax(points)
    MIN_SIZE_LIM = np.amin(points)
    ax.set_xlim(MIN_SIZE_LIM*0.95, MAX_SIZE_LIM*1.05)
    ax.set_ylim(MIN_SIZE_LIM*0.95, MAX_SIZE_LIM*1.05)

    polygon = patches.Polygon(points, linewidth=1, edgecolor='red', fill=False)
    ax.add_patch(polygon)
    plt.show()

if (__name__=='__main__'):
    polygons = random_polygons(3, 10)
    for polygon in polygons:
        draw_polygon(polygon)