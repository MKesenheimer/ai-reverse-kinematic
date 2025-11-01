import numpy as np
from robot import RobotState
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
import functions
import paper_model_data

##########################################################################################
# Roboterarm initialisieren                                                              #
##########################################################################################
# TODO: Parameter des physikalischen Modells hier eintragen
robotState = RobotState()
robotState.set_length_arm1(120)
robotState.set_base_position_arm1((200, 0))
robotState.set_angle_in_grad_arm1(0.1)

robotState.set_length_arm2(75)
robotState.set_angle_in_grad_arm2(0.1)

robotState.set_length_arm3(50)
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

# TODO @Daniel: Hier bitte die gemessenen Werte eintragen
# Trainingsdaten von Hand bestimmen (aus Papiermodell)
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

# train model - micture density network
#network = MixtureDensityNetwork(input_dim=2, output_dim=3, num_epochs=200)
#model = network.train(train_list_coord, train_list_alpha)

# train model - sequential network
network = SequentialNetwork(input_dim=2, output_dim=3, num_epochs=200)
model = network.train(train_list_coord, train_list_alpha)

##########################################################################################
# Test des Trainings                                                                     #
##########################################################################################
while True:
    try:
        # Benutzereingabe
        X = float(input("X-Position eingeben: "))
        Y = float(input("Y-Position eingeben: "))
        print("\n(KNN) Koordinaten: X" + str(X) + " Y" + str(Y))

        # Koordinaten skalieren
        X = functions.scale_coord_to_knn(X, max_length)
        Y = functions.scale_coord_to_knn(Y, max_length)
        test_x_y = np.array([[ X, Y ]])
        print(f"(KNN) Koordinaten: {test_x_y}")

        # Vorhersage aus Modell erzeugen
        params = model.predict(test_x_y)
        knn_alphas = network.sample_from_output(params)
        # skaliere zu den korrekten Einheiten (Grad)
        alpha_bestimmt = functions.scale_knn_to_angle_list(knn_alphas)

        # Kontrolle durch physikalisches Modell
        for alphas in alpha_bestimmt:
            angle1, angle2, angle3 = alphas
            robotState.set_angle_in_grad_arm1(angle1)
            robotState.set_angle_in_grad_arm2(angle2)
            robotState.set_angle_in_grad_arm3(angle3)
            x3_top, y3_top = robotState.get_relative_top_arm3()

            print("\n")
            print(f"(KNN) Winkelvorhersage:       {float(angle1), float(angle2), float(angle3)} Grad")
            print(f"(MOD) Kontrolle durch Modell: {x3_top, y3_top} cm")
    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)
