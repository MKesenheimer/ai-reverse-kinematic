import numpy as np
from robot import RobotState
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
from tensorflow import keras
import functions
import math
import os

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
# Laden der Parameter des KNNs                                                           #
##########################################################################################
print("\nDas sind alle forhandenen Dateien.")
parmater_files = os.listdir("KNN-models")
for f in parmater_files:
    print(f)

data_name = input("\nWelches KNN Model soll geladen werden? >> ")
for x in range(len(parmater_files)):
    if parmater_files[x] == data_name:
        print(f"{data_name} wird geladen...")
        break
    else:
        print('suche...')

network = SequentialNetwork(input_dim=2, output_dim=3, num_epochs=200)
model = keras.models.load_model(f"KNN-models/{data_name}.keras")

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

        # rechne X und Y in Koordinaten des rotierten Koordinatensystem um X, Y -> Xs, Ys
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
        beta_grad  = functions.scale_rad_to_grad(beta)

        # Kontrolle durch physikalisches Modell
        for angle1_grad, angle2_grad, angle3_grad in alpha_grad:
            angle1_grad = float(angle1_grad)
            angle2_grad = float(angle2_grad)
            angle3_grad = float(angle3_grad)
            print(f"Winkelvorhersage (alpha1, alpha2, alpha3, beta): {angle1_grad, angle2_grad, angle3_grad, beta_grad} Grad")

            print("Kontrolle durch Modell:")
            robotState.set_angle_in_grad_arm1(angle1_grad)
            robotState.set_angle_in_grad_arm2(angle2_grad)
            robotState.set_angle_in_grad_arm3(angle3_grad)
            Xs3_top, Zs3_top = robotState.get_relative_top_arm3()

            # rücktransformation in das raumfeste KS: Xs, Ys -> X, Y
            X3_top = Xs3_top * math.cos(beta) - Ys * math.sin(beta)
            Y3_top = Xs3_top * math.sin(beta) + Ys * math.cos(beta)
            Z3_top = Zs3_top
            print(f"Koordinaten im raumfesten KS: X{X3_top} Y{Y3_top} Z{Z3_top}\n")
    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)
