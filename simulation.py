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
while True:
    angle1 = robotState.get_angle_arm1() + 0.01
    robotState.set_angle_arm1(angle1)
    angle2 = robotState.get_angle_arm2() + 0.02
    robotState.set_angle_arm2(angle2)
    angle3 = robotState.get_angle_arm3() + 0.03
    robotState.set_angle_arm3(angle3)
    x_top, y_top = tuple(x - y for x, y in zip(robotState.get_top_arm3(), robotState.get_base_position_arm1()))
    y_top = -y_top
    print(f"alpha = ({angle1 % (2 * math.pi):.1f}, {angle2 % (2 * math.pi):.1f}, {angle3 % (2 * math.pi):.1f}), (x, y) = ({x_top:.1f}, {y_top:.1f})")
    time.sleep(0.02)

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

# train model on test data
alpha = np.array([[0, 0], [1, 0], [0, 1]])
coord = np.array([[0, 0], [1, 0], [1, 1]])

model.fit(coord, alpha, epochs=10, batch_size=8)

print("Trainingsdaten:\nalpha:")
print(alpha)
print("Koordinaten:")
print(coord)

print("\nBerchnete Winkel:")
y = model(coord)
print(y)
