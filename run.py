import numpy as np
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
from gcodeSender import sendGcode
from tensorflow import keras
import functions
import math
import os
import json

##########################################################################################
# Parameter                                                                              #
##########################################################################################
# Maximale Länge des Roboterarms in cm
def load_model_data(filename="model_data.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    max_length = data.get("max_length")
    return max_length
max_length = load_model_data()

##########################################################################################
# Laden der Parameter des KNNs                                                           #
##########################################################################################
print("\nDas sind alle forhandenen Dateien:")
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

network = SequentialNetwork(input_dim=2, output_dim=2, num_epochs=200)
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
        for angle1_grad, angle2_grad in alpha_grad:
            angle1_grad = float(angle1_grad)
            angle2_grad = float(angle2_grad)
            print(f"Winkelvorhersage (beta, alpha1, alpha2): {beta_grad, angle1_grad, angle2_grad} Grad")

            # TODO:
            # An der Stelle Kommunikation mit dem "echten" Roboterarm einfügen
            # -> GCodes an den Roboterarm senden
            # bspw.:
            # G0 Z<beta_grad>
            # G0 A<angle1_grad>
            # G0 B<angle2_grad>
            sendGcode(f"G0 Z{beta_grad} A{angle1_grad} B{angle2_grad}")

    except ValueError as e:
        print("Keine gültige Position. Erneut versuchen.")
        print(e)