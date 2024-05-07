from typing import Tuple, Iterable, List
import numpy as np
import sympy as sm


def mod_add(x: Tuple[int], y: Tuple[int], mod: int):
    """Modular add of two vector tuples, such that the resulting vector has the same lenght as the smallest"""
    return tuple((xi + yi) % mod for xi, yi in zip(x, y))


def mod_add_mult(x_p: Iterable[Tuple[int]], mod: int):
    total = None
    for xi in x_p:
        total = mod_add(total, xi, mod) if total else xi
    return total


def mod_sub(x: Tuple[int], y: Tuple[int], mod: int):
    """Modular substraction of two vector tuples, such that the resulting vector has the same lenght as the smallest"""
    return tuple((xi - yi) % mod for xi, yi in zip(x, y))


def mod_prod(x: Tuple[int], k: int, mod: int):
    return tuple((k * xi) % mod for xi in x)


def is_zero(x: Tuple[int]):
    return all(xi == 0 for xi in x)


def is_linear_indepent(v: Iterable):
    """Checks that the list of vectors, v, passed is linearly independent"""
    matrix = np.matrix(v)
    _, inds = sm.Matrix(matrix).T.rref()  # <found on the internet>
    return len(inds) == len(v)


def cartesian_reference(n: int):
    """
    Generate the cartesian reference for an (Zm)^n space, such that the origin is at 0, and its a standart basis.
    Result: 0, [e0, e1, ...en-1]
    """
    point = np.zeros(n, dtype=int)
    reference = [point.copy()]
    for k in range(n):
        point[k] = 1
        reference.append(point.copy())
        point[k] = 0
    return reference[0], reference[1:]


def simple_affine_space_gen(n: int, m: int):
    p0, base = cartesian_reference(n)
    return generate_mod_affine_space(p0, base, m)


def generate_mod_affine_space(p0, base: Iterable, mod: int):
    affine_space = [tuple(p0)]
    new_points = []
    for ei in base:
        for vk in (mod_prod(ei, k, mod) for k in range(1, mod)):
            new_points.extend((mod_add(p, vk, mod) for p in affine_space))
        affine_space.extend(new_points)
        new_points = []
    return affine_space


def affine_to_cartesian(affine_reference: List[Tuple[int]], mod: int):
    p0 = affine_reference[0]
    vector = (mod_sub(p, p0, mod) for p in affine_reference[1:])
    vector = [v for v in vector if not is_zero(v)]
    if not vector:
        return p0, []
    base = [vector[0]]
    for vi in vector[1:]:
        new_base = base + [vi]
        if is_linear_indepent(new_base):
            base = new_base
    return p0, base


def add_points(p, v: Tuple[int], mod: int):
    if isinstance(p, list):
        return [add_points(item, v, mod) for item in p]
    return [mod_add(p, mod_prod(v, i, mod), mod) for i in range(mod)]


def generate_affine_space_structure(affine_reference: Iterable[Tuple[int]], mod: int):
    """Generates an affine space, from the reference provided with the structure defined in lines, planes, hyperplanes"""
    p0, base = affine_to_cartesian(tuple(affine_reference), mod)
    points = p0
    if not base:
        return points
    for vi in base:
        points = add_points(points, vi, mod)
    return points


if __name__ == "__main__":
    generate_affine_space_structure(
        [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)], 3
    )
