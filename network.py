import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
try:
    import tensorflow_probability as tfp
except ImportError:
    print("Warning: tensorflow-probability could not be imported.")
import matplotlib.pyplot as plt # Liniendiagramm

if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")

def plot_history(history):
    fig, ax1 = plt.subplots()

    # First y-axis: accuracy
    try:
        ax1.plot(
            range(len(history.history['accuracy'])),
            history.history['accuracy'],
            label="accuracy",
            color="blue",
            linewidth=2
        )
        ax1.set_ylabel("Accuracy", color="blue")
    except KeyError:
        pass

    # Second y-axis: loss
    ax2 = ax1.twinx()
    ax2.plot(
        range(len(history.history['loss'])),
        history.history['loss'],
        label="loss",
        color="red",
        linewidth=2
    )
    ax2.set_ylabel("Loss", color="red")

    # Titles and labels
    plt.title("KNN infos")
    ax1.set_xlabel("Zeitlinie")

    # Legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Grid and show
    ax1.grid(True)
    plt.show(block=False)

## define mixture density model for non-bijective data sets
class MixtureDensityNetwork():
    def __init__(self, input_dim, output_dim, num_epochs):
        # model parameters
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_components = 2
        self.num_epochs = num_epochs

    def build_gmm(self, params):
        # Unpack params (same as in loss)
        loc_end = self.num_components * self.output_dim
        scale_end = loc_end + self.num_components * self.output_dim
        logits_end = scale_end + self.num_components

        loc = tf.reshape(params[..., :loc_end], [-1, self.num_components, self.output_dim])
        scale = tf.nn.softplus(tf.reshape(params[..., loc_end:scale_end], [-1, self.num_components, self.output_dim]))
        logits = tf.reshape(params[..., scale_end:logits_end], [-1, self.num_components])

        # Build GMM
        mvn = tfp.distributions.MultivariateNormalDiag(loc=loc, scale_diag=scale)
        gmm = tfp.distributions.MixtureSameFamily(
            mixture_distribution=tfp.distributions.Categorical(logits=logits),
            components_distribution=mvn
        )
        return gmm

    def nll_loss(self, y_true, params):
        # Loss function
        gmm = self.build_gmm(params)
        return -gmm.log_prob(y_true)

    def train(self, training_set_in, training_set_out):
        # Model definition
        inputs = tf.keras.Input(shape=(self.input_dim,))
        x = tf.keras.layers.Dense(64, activation='relu')(inputs)
        #x = tf.keras.layers.Dropout(0.05)(x)
        x = tf.keras.layers.Dense(32, activation='relu')(x)
        #x = tf.keras.layers.Dropout(0.05)(x)

        # Each component has: loc (3), scale (3), + logits (1)
        # Total: num_components * (loc + scale) + logits
        param_size = self.num_components * (2 * self.output_dim) + self.num_components
        params = tf.keras.layers.Dense(param_size)(x)
        model = tf.keras.Model(inputs=inputs, outputs=params)

        # Compile and train
        model.compile(optimizer='adam', loss=self.nll_loss, metrics=['accuracy'])
        history = model.fit(training_set_in, training_set_out, epochs=self.num_epochs, batch_size=2)

        # plotte die trainingsmetrik
        plot_history(history=history)

        return model

    def sample_from_output(self, params, num_samples=1):
        gmm = self.build_gmm(params)

        # Sample outputs
        samples = gmm.sample(num_samples)  # Shape: [num_samples, batch_size, output_dim]
        return [x[0] for x in samples.numpy()]

## define Sequential model with 3 layers
class SequentialNetwork():
    def __init__(self, input_dim, output_dim, num_epochs):
        # model parameters
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_epochs = num_epochs

    def train(self, training_set_in, training_set_out):
        model = keras.Sequential(
            [
                layers.Dense(64, activation="relu", name="layer1", input_shape=(self.input_dim,)),
                #layers.Dropout(0.05),
                layers.Dense(32, activation="relu", name="layer2"),
                #layers.Dropout(0.05),
                layers.Dense(self.output_dim, activation='linear', name="layer3"),
            ]
        )

        # compile
        #model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        model.compile(optimizer='adam', loss='mean_absolute_percentage_error', metrics=['accuracy'])

        # summary
        model.summary()
        #keras.utils.plot_model(model, "my_first_model_with_shape_info_test.png", show_shapes=True)

        # Trainiere das Modell auf die generierte Liste
        history = model.fit(training_set_in, training_set_out, epochs=self.num_epochs, batch_size=2) # (49.1, 21.0, 74.2), (x, y) = (-34.6, 128.0)

        # plotte die trainingsmetrik
        plot_history(history=history)

        return model

    def sample_from_output(self, params, num_samples=1):
        # dummy function
        return params