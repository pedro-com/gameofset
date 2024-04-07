from typing import Tuple
import numpy as np
def mod_add(x: Tuple[int], y: Tuple[int], z: int):
    '''Modular add of two vector tuples, such that the resulting vector has the same lenght as the smallest'''
    return tuple((xi + yi)%z for xi, yi in zip(x, y))

def mod_sub(x: Tuple[int], y: Tuple[int], z: int):
    '''Modular substraction of two vector tuples, such that the resulting vector has the same lenght as the smallest'''
    return tuple((xi - yi)%z for xi, yi in zip(x, y))

def is_zero(x: Tuple[int]):
    return all(xi == 0 for xi in x)

def cartesian_reference(n:int):
    '''
    Generate the cartesian reference for an (Zm)^n space, such that the origin is at 0, and its a standart basis.
    Result: [0, e0, e1, ...en-1]
    '''
    zero = np.zeros(n, dtype=int)
    reference = [zero.copy()]
    for k in range(n):
        zero[k] = 1
        reference.append(zero.copy())
        zero[k] = 0
    return reference

def affine_space_points(n:int, m:int, to_tuple:bool = True):
    reference = cartesian_reference(n)
    affine_space = [reference.pop(0)]
    for ei in reference:
        k_vectors = (k*ei for k in range(m))
        affine_space.extend([[p + vk for p in affine_space] for vk in k_vectors])
    if to_tuple:
        return [tuple(p) for p in affine_space]
    return affine_space

