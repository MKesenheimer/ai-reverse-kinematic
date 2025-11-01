import numpy as np
from robot import RobotState
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
import functions
import paper_model_data
import math

##########################################################################################
# Roboterarm initialisieren                                                              #
##########################################################################################
# TODO: Parameter des physikalischen Modells hier eintragen
robotState = RobotState()
robotState.set_length_arm1(7.0)
robotState.set_base_position_arm1((200, 0))
robotState.set_angle_in_grad_arm1(0.1)

robotState.set_length_arm2(7.0)
robotState.set_angle_in_grad_arm2(0.1)

robotState.set_length_arm3(7.0)
robotState.set_angle_in_grad_arm3(0.1)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

##########################################################################################
# Datensatz fürs Training erzeugen                                                       #
##########################################################################################
# Generiere den Datensatz aus einem Physikmodell für das Training des Roboterarms
#scale = 2
#train_list_alpha = []
#train_list_coord = []
#for angle1 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
#    for angle2 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
#        for angle3 in [x / scale for x in range(0, int(2 * math.pi * scale + 1), 1)]:
#            print(f"alpha = {angle1}, {angle2}, {angle3}")
#            robotState.set_angle_arm1(angle1)
#            robotState.set_angle_arm2(angle2)
#            robotState.set_angle_arm3(angle3)
#            #time.sleep(0.1)
#
#            x1_top, y1_top = robotState.get_relative_top_arm1()
#            x2_top, y2_top = robotState.get_relative_top_arm2()
#            x3_top, y3_top = robotState.get_relative_top_arm3()
#
#            if y1_top >= 0 and y2_top >= 0 and y3_top >= 0:
#                print(f" {len(train_list_alpha)} -> alpha = ({angle1:.1f}, {angle2:.1f}, {angle3:.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")
#                # Skaliere die Winkel auf den Bereich [0, 1]
#                angle1_scaled = scale_angle_to_knn(angle1)
#                angle2_scaled = scale_angle_to_knn(angle2)
#                angle3_scaled = scale_angle_to_knn(angle3)
#                train_list_alpha.extend([(angle1_scaled, angle2_scaled, angle3_scaled)])
#                # Skaliere die Koordinaten auf den Bereich [0, 1]
#                x3_top_scaled = scale_coord_to_knn(x3_top, max_length)
#                y3_top_scaled = scale_coord_to_knn(y3_top, max_length)
#                train_list_coord.extend([(x3_top_scaled, y3_top_scaled)])
#            else:
#                print(f" {len(train_list_alpha)} -> der arm ist im boden!")

# Trainingsdaten von Hand bestimmt (aus Papiermodell)
# Einheiten:
# Winkel in Grad
# Abstände in cm
train_list_alpha = paper_model_data.list_alpha
train_list_coord = paper_model_data.list_coord

print(train_list_alpha)
print(train_list_coord)

##########################################################################################
# Training des KNNs                                                                      #
##########################################################################################
# automatische Umrechnung von Winkel in Grad zu Werten zwischen [0, 1]
train_list_alpha = functions.scale_angle_list_to_knn(train_list_alpha)
# automatische Umrechnung der Koordinaten in Werten zwischen [0, 1]
train_list_coord = functions.scale_coord_list_to_knn(train_list_coord, max_length)

# Datensätze für das Training in das richtige Format bringen
train_list_alpha = np.array(train_list_alpha)
train_list_coord = np.array(train_list_coord)

# DEBUG
#print(functions.scale_knn_to_angle_list(train_list_alpha))
#print(functions.scale_knn_to_coord_list(train_list_coord, max_length))
#exit(0)

# train model - mixture density network
#network = MixtureDensityNetwork(input_dim=2, output_dim=3, num_epochs=200)
#model = network.train(train_list_coord, train_list_alpha)

# train model - sequential network
network = SequentialNetwork(input_dim=2, output_dim=3, num_epochs=2000)
model = network.train(train_list_coord, train_list_alpha)

##########################################################################################
# Test des Trainings                                                                     #
##########################################################################################
print("Hinweis zu den Koordinaten: x-y-Ebene auf dem Boden, z-Achse zeigt nach oben.")
while True:
    try:
        # Benutzereingabe der Koordinaten im raumfesten Koordinatensystem
        X = float(input("X-Position eingeben: "))
        Y = float(input("Y-Position eingeben: "))
        Z = float(input("Z-Position eingeben: "))
        print(f"\nKoordinaten: X{X} Y{Y} Z{Z}")

        # Winkel (in rad) beta für die Rotation um die z-Achse
        # dieser Winkel ist einfach zu berechnen und muss nicht traniert werden!
        beta = functions.beta_from_x_y(X, Y)

        # rechne X und Y in Koordinaten des rotierten Koordinatensystem um -> Xs, Ys
        Xs =  X * math.cos(beta) + Y * math.sin(beta)
        Ys = -X * math.sin(beta) + Y * math.cos(beta)
        Zs = Z
        print(f"Koordinaten im mitrotierenden KS: Xs{Xs} Ys{Ys} Zs{Zs}")

        # Koordinaten skalieren
        xs = functions.scale_coord_to_knn(Xs, max_length)
        ys = functions.scale_coord_to_knn(Ys, max_length)
        zs = functions.scale_coord_to_knn(Zs, max_length)
        test_xs_zs = np.array([[ xs, zs ]])
        print(f"Skalierte Koordinaten im mitrotierenden KS für das KNN: xs{xs} ys{ys} zs{zs}")

        # Vorhersage aus Modell erzeugen
        params = model.predict(test_xs_zs)
        knn_alphas = network.sample_from_output(params)
        # skaliere zu den korrekten Einheiten (Grad)
        alpha_grad = functions.scale_knn_to_angle_list(knn_alphas)

        # Kontrolle durch physikalisches Modell
        for angle1_grad, angle2_grad, angle3_grad in alpha_grad:
            angle1_grad = float(angle1_grad)
            angle2_grad = float(angle2_grad)
            angle3_grad = float(angle3_grad)
            beta_grad = functions.scale_rad_to_grad(beta)
            print(f"Winkelvorhersage (alpha1, alpha2, alpha3, beta): {angle1_grad, angle2_grad, angle3_grad, beta_grad} Grad")

            print("Kontrolle durch Modell:")
            robotState.set_angle_in_grad_arm1(angle1_grad)
            robotState.set_angle_in_grad_arm2(angle2_grad)
            robotState.set_angle_in_grad_arm3(angle3_grad)
            Xs3_top, Zs3_top = robotState.get_relative_top_arm3()

            # rücktransformation in das raumfeste KS -> X, Y
            X3_top = Xs3_top * math.cos(beta) - Ys * math.sin(beta)
            Y3_top = Xs3_top * math.sin(beta) + Ys * math.cos(beta)
            Z3_top = Zs3_top
            print(f"Koordinaten im raumfesten KS: X{X3_top} Y{Y3_top} Z{Z3_top}\n")
    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)
