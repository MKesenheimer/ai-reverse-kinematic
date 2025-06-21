import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Define Sequential model with 3 layers
model = keras.Sequential(
    [
        layers.Dense(2, activation="relu", name="layer1"),
        layers.Dense(3, activation="relu", name="layer2"),
        layers.Dense(4, name="layer3"),
    ]
)


model.summary()

#keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)

# Call model on a test input
x = tf.ones((3, 2))
y = model(x)

print(y)