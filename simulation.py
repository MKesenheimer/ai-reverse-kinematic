import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

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
keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)

# train model on test data
alpha = np.array([[0, 0], [1, 0], [0, 1]])
coord = np.array([[0, 0], [1, 0], [1, 1]])

model.fit(coord, alpha, epochs=1000, batch_size=8)

print("Trainingsdaten")
print(alpha)
print(coord)

print("")
y = model(coord)
print(y)