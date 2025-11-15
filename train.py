import numpy as np
from robot import RobotState
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
from tensorflow import keras
import functions
import paper_model_data
import math
import os

robotState = RobotState()
robotState.set_length_arm1(7.0)
robotState.set_base_position_arm1((200, 0))
robotState.set_angle_in_grad_arm1(0.1)

robotState.set_length_arm2(7.0)
robotState.set_angle_in_grad_arm2(0.1)

robotState.set_length_arm3(7.0)
robotState.set_angle_in_grad_arm3(0.1)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

# Einheiten:
# Winkel in Grad
# Abstände in cm
train_list_alpha = paper_model_data.list_alpha
train_list_coord = paper_model_data.list_coord

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

# train model - micture density network
#network = MixtureDensityNetwork(input_dim=2, output_dim=3, num_epochs=200)
#model = network.train(train_list_coord, train_list_alpha)
print("\nDas sind alle forhandenen Dateien.")
for feil in os.listdir("KNN-models"):
    print(feil)

data_name = input("\nWie soll das KNN Model Heißen?: ")

# train model - sequential network
network = SequentialNetwork(input_dim=2, output_dim=3, num_epochs=200)
model = network.train(train_list_coord, train_list_alpha)

model.save(f"KNN-models\\{data_name}.keras")

##########################################################################################
# Test des Trainings                                                                     #
##########################################################################################
print("Hinweis zu den Koordinaten: x-y-Ebene auf dem Boden, z-Achse zeigt nach oben.")
while True:
    try:
        # Benutzereingabe
        X = float(input("X-Position eingeben: "))
        Y = float(input("Y-Position eingeben: "))
        Z = float(input("Z-Position eingeben: "))
        print(f"\n(KNN) Koordinaten: X{X} Y{Y} Z{Z}")

        # Koordinaten skalieren
        x = functions.scale_coord_to_knn(X, max_length)
        y = functions.scale_coord_to_knn(Y, max_length)
        z = functions.scale_coord_to_knn(Z, max_length)
        test_x_z = np.array([[ x, z ]])
        print(f"(KNN) Koordinaten: {test_x_z}")

        # Vorhersage aus Modell erzeugen
        params = model.predict(test_x_z)
        knn_alphas = network.sample_from_output(params)
        # skaliere zu den korrekten Einheiten (Grad)
        alpha_bestimmt = functions.scale_knn_to_angle_list(knn_alphas)

        # Winkel beta für die Rotation um die z-Achse
        # dieser Winkel ist einfach zu berechnen und muss nicht traniert werden!
        beta = functions.beta_from_x_y(X, Y)

        # Kontrolle durch physikalisches Modell
        for alphas in alpha_bestimmt:
            angle1, angle2, angle3 = alphas
            robotState.set_angle_in_grad_arm1(angle1)
            robotState.set_angle_in_grad_arm2(angle2)
            robotState.set_angle_in_grad_arm3(angle3)
            x3_top, y3_top = robotState.get_relative_top_arm3()

            print("\n")
            print(f"(KNN) Winkelvorhersage (alpha1, alpha2, alpha3, beta):       {float(angle1), float(angle2), float(angle3), float(beta)} Grad")
            print(f"(MOD) Kontrolle durch Modell: {x3_top, y3_top} cm")
    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)
