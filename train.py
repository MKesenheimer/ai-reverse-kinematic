import numpy as np
# based on tensorflow
from network import MixtureDensityNetwork, SequentialNetwork
# based on pytorch (better AMD support)
#from torchnetwork import SequentialNetwork
import functions
import paper_model_data
import os

##########################################################################################
# Parameter                                                                              #
##########################################################################################
# Maximale Länge des Roboterarms in cm
max_length = 21

##########################################################################################
# Datensatz fürs Training erzeugen                                                       #
##########################################################################################
# Trainingsdaten von Hand bestimmt (aus Papiermodell)
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

# train model - mixture density network
#network = MixtureDensityNetwork(input_dim=2, output_dim=3, num_epochs=200)
#model = network.train(train_list_coord, train_list_alpha)
print("\nDas sind alle forhandenen Modelle in KNN-models:")
for f in os.listdir("KNN-models"):
    print(f)

data_name = input("\nWie soll das KNN Model heißen?: ")

# train model - sequential network
network = SequentialNetwork(input_dim=2, output_dim=3, num_epochs=200)
model = network.train(train_list_coord, train_list_alpha)

model.save(f"KNN-models/{data_name}.keras")