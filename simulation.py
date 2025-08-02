import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from robot import RobotState
import time
import math
import random

robotState = RobotState()
robotState.set_length_arm1(100)
robotState.set_base_position_arm1((200, 250))
robotState.set_angle_arm1(0)

robotState.set_length_arm2(75)
robotState.set_angle_arm2(0)

robotState.set_length_arm3(50)
robotState.set_angle_arm3(0)

tren_list = []

# Test: Update den Winkel des Roboterarms:
y1_top = 0
y2_top = 0
y3_top = 0

tren_list_nicht_gefültert = []
for angle1 in range(-3, 3+1, 1):
    for angle2 in range(-3, 3+1, 1):
        for angle3 in range(-3, 3+1, 1):
            tren_list_nicht_gefültert.extend([(angle1, angle2, angle3)])
print(tren_list_nicht_gefültert)

time.sleep(5)

for angle1, angle2, angle3 in tren_list_nicht_gefültert:
    robotState.set_angle_arm1(angle1)
    robotState.set_angle_arm2(angle2)
    robotState.set_angle_arm3(angle3)

    x1_top, y1_top = robotState.get_relative_top_arm1()
    x2_top, y2_top = robotState.get_relative_top_arm2()
    x3_top, y3_top = robotState.get_relative_top_arm3()

    if y1_top >= 0 and y2_top >= 0 and y3_top >= 0:
        print("Fertig: " + str(len(tren_list)) + f" alpha = ({angle1:.1f}, {angle2:.1f}, {angle3:.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")
        tren_list.extend([(angle1, angle2, angle3, x3_top, y3_top)])
    else:
        print("Fertig: " + str(len(tren_list)) + " der arm ist im boden!")

    #time.sleep(0.02)



if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")

# define Sequential model with 3 layers
model = keras.Sequential(
    [
        layers.Dense(32, activation="relu", name="layer1", input_shape=(2,)),
        layers.Dense(16, activation="relu", name="layer2"),
        layers.Dense(3, activation='linear', name="layer3"),
    ]
)

# compile
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# summary
model.summary()
#keras.utils.plot_model(model, "my_first_model_with_shape_info_test.png", show_shapes=True)


# erster Wert erzeugen:
angle1, angle2, angle3 = 0.1, 0.2, 0.3
robotState.set_angle_arm1(angle1)
robotState.set_angle_arm2(angle2)
robotState.set_angle_arm3(angle3)
x3_top, y3_top = robotState.get_relative_top_arm3()

print(f"alpha = ({angle1 % (2 * math.pi):.1f}, {angle2 % (2 * math.pi):.1f}, {angle3 % (2 * math.pi):.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")

tren_angle = []
tren_x_y = []
zeler = 0
for for_angle1, for_angle2, for_angle3, x, y in tren_list:
   tren_angle.extend([(for_angle1, for_angle2, for_angle3)])
   tren_x_y.extend([(x, y)])
   zeler = zeler + 1
   print("Daten werden forbereitet...  " + str(zeler) + " von " + str(len(tren_list)))


tren_angle = np.array(tren_angle)
tren_x_y = np.array(tren_x_y)

model.fit(tren_x_y, tren_angle, epochs=20)# (49.1, 21.0, 74.2), (x, y) = (-34.6, 128.0)

while True:
    X = float(input("X-Position eingeben: "))
    Y = float(input("Y-Position eingeben: "))
    test_x_y = np.array([[ X, Y ]])

    print("\n(KNN) Koordinaten: X" + str(X) + " Y" + str(Y))
    
    alpha_bestimmt = model.predict(test_x_y)

    angle1, angle2, angle3 = alpha_bestimmt[0]
    robotState.set_angle_arm1(angle1)
    robotState.set_angle_arm2(angle2)
    robotState.set_angle_arm3(angle3)
    x3_top, y3_top = robotState.get_relative_top_arm3()

    print("\n(KNN) Berchnete Winkel: " + str(alpha_bestimmt))
    print("kontrole : " + str(robotState.get_relative_top_arm3()))
    





