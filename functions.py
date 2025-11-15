import math

# Skaliere den Winkelbereich [0, 2 Pi] -> [0, 1]
def scale_rad_to_knn(alpha):
    return alpha / (2 * math.pi)

# Skaliere den Winkelbereich des KNN [0, 1] -> [0, 2 Pi]
def scale_knn_to_rad(alpha0):
    return alpha0 * 2 * math.pi

# Skaliere Koordinaten zu Werte des KNN [0, max_length] -> [0, 1]
def scale_coord_to_knn(coord, max_length):
    return coord / max_length

# Skaliere den Winkelbereich des KNN [0, 1] -> [0, max_length]
def scale_knn_to_coord(coord0, max_length):
    return coord0 * max_length

# Rechne Grad in Rad um
def scale_grad_to_rad(alpha):
    return (alpha / 360) * 2 * math.pi

# Rechne Rad in Grad um
def scale_rad_to_grad(alpha0):
    return (alpha0 / (2 * math.pi) * 360)

# scale list of angles in grad to knn values ([0, 1])
def scale_angle_list_to_knn(alphas):
    for j in range(len(alphas)):
        for i in range(len(alphas[j])):
            alphas[j][i] = scale_rad_to_knn(scale_grad_to_rad(alphas[j][i]))
    return alphas

# scale list of angles in knn values ([0, 1]) to list of angles in grad
def scale_knn_to_angle_list(alphas):
    for j in range(len(alphas)):
        for i in range(len(alphas[j])):
            alphas[j][i] = float(scale_rad_to_grad(scale_knn_to_rad(alphas[j][i])))
    return alphas

# scale list of coordinates to knn values ([0, 1]) 
def scale_coord_list_to_knn(coords, max_length):
    for j in range(len(coords)):
        for i in range(len(coords[j])):
            coords[j][i] = scale_coord_to_knn(coords[j][i], max_length)
    return coords

# scale list of coordinates in knn values ([0, 1]) to list of coordinates
def scale_knn_to_coord_list(coords, max_length):
    for j in range(len(coords)):
        for i in range(len(coords[j])):
            coords[j][i] = scale_knn_to_coord(coords[j][i], max_length)
    return coords

# Berechne den Winkel beta in rad aus den Koordinaten X und Y
def beta_from_x_y(X, Y):
    beta = 0
    if X > 0 and Y > 0:
        beta = math.atan(Y / X)
    elif X < 0 and Y > 0:
        beta = math.pi + math.atan(Y / X)
    elif X < 0 and Y < 0:
        beta = 1.5 * math.pi - math.atan(Y / X)
    elif X > 0 and Y < 0:
        beta = 2.0 * math.pi + math.atan(Y / X)
    return beta