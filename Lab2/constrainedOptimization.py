import numpy as np
from pre import point, example, golden_search


def ALM(loss_function: example, start: point, y_t: float, epsilon=0.1, iteration_max=1000) -> list:
    points, M, k = [start], len(start), 0

    while True:
        # find the new point by cyclic coordinate method
        p = points[k]
        p_old = p
        while True:
            direction = [0] * M
            direction[np.mod(k, M)] = 1
            step = golden_search(loss_function, y_t, p, direction)
            p = p + point(direction[0] * step, direction[1] * step)
            points.append(p)
            k += 1
            if k > iteration_max or (points[k] - points[k - 1]).dis() < epsilon: break
        # update the lama
        y_t = y_t + loss_function.rho * loss_function.subject_to(p)
        # if meet the termination condition then break
        if k > iteration_max or (p - p_old).dis() < epsilon: break

    return points


def ADMM(loss_function: example, start: point, y_t: float, epsilon=1e-1, iteration_max=1000) -> list:
    points, k = [start], 0

    while True:
        # update the point
        p = points[k]
        direction = [1, 0]
        step = golden_search(loss_function, y_t, p, direction)
        p = p + point(direction[0] * step, direction[1] * step)
        direction = [0, 1]
        step = golden_search(loss_function, y_t, p, direction)
        p = p + point(direction[0] * step, direction[1] * step)
        points.append(p)
        k += 1
        # update the lama
        y_t = y_t + loss_function.rho * loss_function.subject_to(p)
        # if meet the termination condition then break
        if k > iteration_max or (points[k] - points[k - 1]).dis() < epsilon: break

    return points
