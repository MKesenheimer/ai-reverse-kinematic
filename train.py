import numpy as np
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
import functions
import os
import json

##########################################################################################
# Datensatz fürs Training erzeugen                                                       #
##########################################################################################
# Trainingsdaten mit den Einheiten:
# Winkel in Grad
# Abstände in cm
def load_model_data(filename="model_data.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    train_list_alpha = data.get("list_alpha", [])
    train_list_coord = data.get("list_coord", [])
    max_length = data.get("max_length")
    return train_list_alpha, train_list_coord, max_length

train_list_alpha, train_list_coord, max_length = load_model_data()
output_dimension = len(train_list_alpha[0])
input_dimension = len(train_list_coord[0])

print(f"train_list_alpha = {train_list_coord}")
print(f"train_list_coord = {train_list_coord}")
print(f"max_length = {max_length}")

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

# train model - mixture density network
#network = MixtureDensityNetwork(input_dim=2, output_dim=3, num_epochs=200)
#model = network.train(train_list_coord, train_list_alpha)
print("\nDas sind alle forhandenen Modelle in KNN-models:")
for f in os.listdir("KNN-models"):
    print(f)

data_name = input("\nWie soll das KNN Model heißen?: ")
epochs = int(input("\nMit wie vielen Epochen soll trainiert werden?: "))

# train model - sequential network
network = SequentialNetwork(input_dim=input_dimension, output_dim=output_dimension, num_epochs=epochs)
model = network.train(train_list_coord, train_list_alpha)

model.save(f"KNN-models/{data_name}.keras")