"""
    Module for operations in the Finite Affine Space.
"""
from typing import Tuple, Iterable, List
import numpy as np
import sympy as sm


def mod_addition(x: Tuple[int], y: Tuple[int], m: int):
    """Modular addition of two vector tuples, such that the resulting vector has the same length as the smallest"""
    return tuple((xi + yi) % m for xi, yi in zip(x, y))


def mod_mult_addition(x_p: Iterable[Tuple[int]], m: int):
    """Modular addition of multiple vectors"""
    total = None
    for xi in x_p:
        total = mod_addition(total, xi, m) if total else xi
    return total


def mod_substraction(x: Tuple[int], y: Tuple[int], m: int):
    """Modular substraction of two vector tuples, such that the resulting vector has the same lenght as the smallest"""
    return tuple((xi - yi) % m for xi, yi in zip(x, y))


def mod_product(x: Tuple[int], k: int, m: int):
    """Modular scalar product between a value k and a vector x"""
    return tuple((k * xi) % m for xi in x)


def is_zero(x: Tuple[int]):
    """Checks if the vector x is zero."""
    return all(xi == 0 for xi in x)


def is_linear_indepent(v: Iterable):
    """Checks that the list of vectors, v, passed is linearly independent"""
    matrix = np.matrix(v)
    _, inds = sm.Matrix(matrix).T.rref()
    return len(inds) == len(v)


def cartesian_reference(n: int):
    """
    Generate the cartesian reference for an (Zm)^n space, such that the origin is at 0, and its a standart basis.
    Result: 0, [e0, e1, ...en-1]
    """
    point = np.zeros(n, dtype=int)
    reference = [point.copy()]
    # Adds e_k to the vector base
    for k in range(n):
        point[k] = 1
        reference.append(point.copy())
        point[k] = 0
    return reference[0], reference[1:]

def generate_mod_affine_space(p0, base: Iterable, m: int):
    """Generate all the points in an affine finite space of order m, centered at p0 and the group of vectors, base"""
    affine_space = [tuple(p0)]
    new_points = []
    # Add new points every iteration, by adding the vector v_k from the vector base
    for ei in base:
        for vk in (mod_product(ei, k, m) for k in range(1, m)):
            new_points.extend((mod_addition(p, vk, m) for p in affine_space))
        affine_space.extend(new_points)
        new_points = []
    return affine_space

def simple_affine_space_gen(n: int, m: int):
    """Generate all the points for an affine finite space AG(n, m)"""
    p0, base = cartesian_reference(n)
    return generate_mod_affine_space(p0, base, m)


def affine_to_cartesian(affine_reference: List[Tuple[int]], m: int):
    """Transforms an affine reference of points into a cartesian reference."""
    p0 = affine_reference[0]
    vector = (mod_substraction(p, p0, m) for p in affine_reference[1:])
    vector = [v for v in vector if not is_zero(v)]
    if not vector:
        return p0, []
    base = [vector[0]]
    for vi in vector[1:]:
        new_base = base + [vi]
        if is_linear_indepent(new_base):
            base = new_base
    return p0, base


def _add_points(current_points: Iterable, v: Tuple[int], m: int):
    """
    Recursive function to add new points to the current_points. If current_points is a single point, adds the line of
    points generated from the point in current points and the vector v. If current_points is a list of items, where an
    item could be either a point or another list of points, calls _add_points in said items.
    """
    if isinstance(current_points, list):
        return [_add_points(item, v, m) for item in current_points]
    return [mod_addition(current_points, mod_product(v, i, m), m) for i in range(m)]


def generate_affine_space_structure(affine_reference: Iterable[Tuple[int]], m: int):
    """
    Generates an affine finite space from the reference provided with the structure defined in lines, planes, hyperplanes.
    """
    p0, base = affine_to_cartesian(tuple(affine_reference), m)
    points = p0
    if not base:
        return points
    for vi in base:
        points = _add_points(points, vi, m)
    return points


if __name__ == "__main__":
    generate_affine_space_structure(
        [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)], 3
    )
