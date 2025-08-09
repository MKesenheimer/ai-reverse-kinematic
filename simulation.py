import numpy as np
from robot import RobotState
from network import mixture_density_network, sequential_network
import math

# Skaliere den Winkelbereich [0, 2 Pi] -> [0, 1]
def scale_angle_to_knn(alpha):
    return alpha / (2 * math.pi)

# Skaliere den Winkelbereich des KNN [0, 1] -> [0, 2 Pi]
def scale_knn_to_angle(alpha0):
    return alpha0 * 2 * math.pi

# Skaliere Koordinaten zu Werte des KNN [0, max_length] -> [0, 1]
def scale_coord_to_knn(coord, max_length):
    return coord / max_length

# Skaliere den Winkelbereich des KNN [0, 1] -> [0, max_length]
def scale_knn_to_coord(coord0, max_length):
    return coord0 * max_length

# Initialisiere den Roboterarm
robotState = RobotState()
robotState.set_length_arm1(120)
robotState.set_base_position_arm1((200, 250))
robotState.set_angle_arm1(0)

robotState.set_length_arm2(75)
robotState.set_angle_arm2(0)

robotState.set_length_arm3(50)
robotState.set_angle_arm3(0)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

# Generiere den Datensatz für das Training des Roboterarms
scale = 2
train_list_alpha = []
train_list_coord = []
for angle1 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
    for angle2 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
        for angle3 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
            print(f"alpha = {angle1}, {angle2}, {angle3}")
            robotState.set_angle_arm1(angle1)
            robotState.set_angle_arm2(angle2)
            robotState.set_angle_arm3(angle3)
            #time.sleep(0.1)

            x1_top, y1_top = robotState.get_relative_top_arm1()
            x2_top, y2_top = robotState.get_relative_top_arm2()
            x3_top, y3_top = robotState.get_relative_top_arm3()

            if y1_top >= 0 and y2_top >= 0 and y3_top >= 0:
                print(f" {len(train_list_alpha)} -> alpha = ({angle1:.1f}, {angle2:.1f}, {angle3:.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")
                # Skaliere die Winkel auf den Bereich [0, 1]
                angle1_scaled = scale_angle_to_knn(angle1)
                angle2_scaled = scale_angle_to_knn(angle2)
                angle3_scaled = scale_angle_to_knn(angle3)
                train_list_alpha.extend([(angle1_scaled, angle2_scaled, angle3_scaled)])
                # Skaliere die Koordinaten auf den Bereich [0, 1]
                x3_top_scaled = scale_coord_to_knn(x3_top, max_length)
                y3_top_scaled = scale_coord_to_knn(y3_top, max_length)
                train_list_coord.extend([(x3_top_scaled, y3_top_scaled)])
            else:
                print(f" {len(train_list_alpha)} -> der arm ist im boden!")

# Datensätze für das Training
train_list_alpha = np.array(train_list_alpha)
train_list_coord = np.array(train_list_coord)

# train model
network = mixture_density_network(input_dim=2, output_dim=3, num_epochs=2000)
#network = sequential_network(input_dim=2, output_dim=3, num_epochs=100)
model = network.train(train_list_coord, train_list_alpha)

while True:
    try:
        X = float(input("X-Position eingeben: "))
        Y = float(input("Y-Position eingeben: "))
        print("\n(KNN) Koordinaten: X" + str(X) + " Y" + str(Y))

        X = scale_coord_to_knn(X, max_length)
        Y = scale_coord_to_knn(Y, max_length)
        test_x_y = np.array([[ X, Y ]])
        print(f"(KNN) Koordinaten: {test_x_y}")

        # Get model output parameters
        params = model.predict(test_x_y)  # shape: [1, param_size]
        alpha_bestimmt = network.sample_from_output(params, num_samples=5)

        print(f"Ausgabe KNN type: {type(alpha_bestimmt)}")
        print("Sampled outputs:\n", alpha_bestimmt)

        for alphas in alpha_bestimmt:
            angle1, angle2, angle3 = alphas
            angle1 = scale_knn_to_angle(angle1)
            angle2 = scale_knn_to_angle(angle2)
            angle3 = scale_knn_to_angle(angle3)

            robotState.set_angle_arm1(angle1)
            robotState.set_angle_arm2(angle2)
            robotState.set_angle_arm3(angle3)
            x3_top, y3_top = robotState.get_relative_top_arm3()

            print(f"\n(KNN) Berchnete Winkel: {angle1, angle2, angle3}")
            print("kontrole : " + str(robotState.get_relative_top_arm3()))
    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)
