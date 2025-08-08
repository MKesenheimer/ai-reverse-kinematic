import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_probability as tfp
from robot import RobotState
import math
import sys
import time

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

robotState = RobotState()
robotState.set_length_arm1(120)
robotState.set_base_position_arm1((200, 250))
robotState.set_angle_arm1(0)

robotState.set_length_arm2(75)
robotState.set_angle_arm2(0)

robotState.set_length_arm3(50)
robotState.set_angle_arm3(0)
max_length = robotState.get_length_arm1() + robotState.get_length_arm2() + robotState.get_length_arm3()

# Test: Update den Winkel des Roboterarms:
y1_top = 0
y2_top = 0
y3_top = 0

scale = 2
train_list_alpha = []
train_list_coord = []
#for angle1 in range(-3, 3+1, 1):
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


train_list_alpha = np.array(train_list_alpha)
train_list_coord = np.array(train_list_coord)

# Bereite das neuronale Netz vor
if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")



# Mixture model setup
num_components = 3
output_dim = 3

def mdn_output(params):
    loc = params[..., :num_components * output_dim]
    scale = tf.nn.softplus(params[..., num_components * output_dim:-num_components])
    mix_logits = params[..., -num_components:]

    loc = tf.reshape(loc, [-1, num_components, output_dim])
    scale = tf.reshape(scale, [-1, num_components, output_dim])

    mvn = tfp.distributions.MultivariateNormalDiag(loc=loc, scale_diag=scale)
    mix = tfp.distributions.Categorical(logits=mix_logits)
    gmm = tfp.distributions.MixtureSameFamily(mixture_distribution=mix, components_distribution=mvn)
    return gmm

def nll_loss(y_true, gmm):
    return -gmm.log_prob(y_true)

# Build model
inputs = tf.keras.Input(shape=(2,))
x = tf.keras.layers.Dense(64, activation='relu')(inputs)
x = tf.keras.layers.Dense(64, activation='relu')(x)
params = tf.keras.layers.Dense((num_components * (output_dim + 1)) + num_components)(x)  # loc + scale + mix

gmm = tf.keras.layers.Lambda(mdn_output)(params)

model = tf.keras.Model(inputs=inputs, outputs=gmm)
model.add_loss(nll_loss(tf.keras.Input(shape=(output_dim,)), gmm))
model.compile(optimizer='adam')

model.fit(train_list_coord, train_list_alpha, epochs=2000)

## define Sequential model with 3 layers
#model = keras.Sequential(
#    [
#        layers.Dense(32, activation="relu", name="layer1", input_shape=(2,)),
#        layers.Dense(16, activation="relu", name="layer2"),
#        layers.Dense(3, activation='linear', name="layer3"),
#    ]
#)
#
## compile
#model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
#
## summary
#model.summary()
##keras.utils.plot_model(model, "my_first_model_with_shape_info_test.png", show_shapes=True)
#
## Trainiere das Modell auf die generierte Liste
#model.fit(train_list_coord, train_list_alpha, epochs=2000) # (49.1, 21.0, 74.2), (x, y) = (-34.6, 128.0)

while True:
    try:
        X = float(input("X-Position eingeben: "))
        Y = float(input("Y-Position eingeben: "))
        print("\n(KNN) Koordinaten: X" + str(X) + " Y" + str(Y))

        X = scale_coord_to_knn(X, max_length)
        Y = scale_coord_to_knn(Y, max_length)
        test_x_y = np.array([[ X, Y ]])

        alpha_bestimmt = model.predict(test_x_y)
        angle1, angle2, angle3 = alpha_bestimmt[0]
        angle1 = scale_knn_to_angle(angle1)
        angle2 = scale_knn_to_angle(angle2)
        angle3 = scale_knn_to_angle(angle3)

        robotState.set_angle_arm1(angle1)
        robotState.set_angle_arm2(angle2)
        robotState.set_angle_arm3(angle3)
        x3_top, y3_top = robotState.get_relative_top_arm3()

        print("\n(KNN) Berchnete Winkel: " + str(alpha_bestimmt))
        print("kontrole : " + str(robotState.get_relative_top_arm3()))
    except ValueError:
        print("Keine gültige Position. Erneut versuchen.")
