import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from robot import RobotState
import time
import math

robotState = RobotState()
robotState.set_length_arm1(100)
robotState.set_base_position_arm1((200, 250))
robotState.set_angle_arm1(0)

robotState.set_length_arm2(75)
robotState.set_angle_arm2(0)

robotState.set_length_arm3(50)
robotState.set_angle_arm3(0)


# Test: Update den Winkel des Roboterarms:
#y1_top = 0
#y2_top = 0
#y3_top = 0
#while True:
#    if y1_top >= 0 and y2_top >= 0 and y3_top >= 0:
#        angle1 = robotState.get_angle_arm1() + 0.01
#        robotState.set_angle_arm1(angle1)
#        angle2 = robotState.get_angle_arm2() + 0.02
#        robotState.set_angle_arm2(angle2)
#        angle3 = robotState.get_angle_arm3() - 0.03
#        robotState.set_angle_arm3(angle3)
#
#    x1_top, y1_top = robotState.get_relative_top_arm1()
#    x2_top, y2_top = robotState.get_relative_top_arm2()
#    x3_top, y3_top = robotState.get_relative_top_arm3()
#
#    print(f"alpha = ({angle1 % (2 * math.pi):.1f}, {angle2 % (2 * math.pi):.1f}, {angle3 % (2 * math.pi):.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")
#    time.sleep(0.02)

if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")

# define Sequential model with 3 layers
model = keras.Sequential(
    [
        layers.Dense(32, activation="relu", name="layer1", input_shape=(2,)),
        layers.Dense(16, activation="relu", name="layer2"),
        layers.Dense(2, activation='sigmoid', name="layer3"),
    ]
)

# compile
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# summary
model.summary()
keras.utils.plot_model(model, "my_first_model_with_shape_info_test.png", show_shapes=True)


# erster Wert erzeugen:
angle1, angle2, angle3 = 0.1, 0.2, 0.3
robotState.set_angle_arm1(angle1)
robotState.set_angle_arm2(angle2)
robotState.set_angle_arm3(angle3)
x3_top, y3_top = robotState.get_relative_top_arm3()

print(f"alpha = ({angle1 % (2 * math.pi):.1f}, {angle2 % (2 * math.pi):.1f}, {angle3 % (2 * math.pi):.1f}), (x, y) = ({x3_top:.1f}, {y3_top:.1f})")


# train model on test data
alpha = np.array([[0, 0], [1, 0], [0, 1]])
coord = np.array([[0, 0], [1, 0], [1, 1]])

model.fit(coord, alpha, epochs=10, batch_size=8)

print("Trainingsdaten:\nalpha:")
print(alpha)
print("Koordinaten:")
print(coord)

print("\nBerchnete Winkel:")
alpha_bestimmt = model(coord)
print(alpha_bestimmt)
