import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_probability as tfp

if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")

## define mixture density model for non-bijective data sets
class mixture_density_network():
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
        x = tf.keras.layers.Dense(64, activation='relu')(x)

        # Each component has: loc (3), scale (3), + logits (1)
        # Total: num_components * (loc + scale) + logits
        param_size = self.num_components * (2 * self.output_dim) + self.num_components
        params = tf.keras.layers.Dense(param_size)(x)
        model = tf.keras.Model(inputs=inputs, outputs=params)

        # Compile and train
        model.compile(optimizer='adam', loss=self.nll_loss)
        model.fit(training_set_in, training_set_out, epochs=self.num_epochs, batch_size=2)
        return model

    def sample_from_output(self, params, num_samples=1):
        gmm = self.build_gmm(params)

        # Sample outputs
        samples = gmm.sample(num_samples)  # Shape: [num_samples, batch_size, output_dim]
        return samples.numpy()

## define Sequential model with 3 layers
class sequential_network():
    def __init__(self, input_dim, output_dim, num_epochs):
        # model parameters
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_epochs = num_epochs

    def train(self, training_set_in, training_set_out):
        model = keras.Sequential(
            [
                layers.Dense(32, activation="relu", name="layer1", input_shape=(self.input_dim,)),
                layers.Dense(16, activation="relu", name="layer2"),
                layers.Dense(self.output_dim, activation='linear', name="layer3"),
            ]
        )

        # compile
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        # summary
        #model.summary()
        #keras.utils.plot_model(model, "my_first_model_with_shape_info_test.png", show_shapes=True)

        # Trainiere das Modell auf die generierte Liste
        model.fit(training_set_in, training_set_out, epochs=self.num_epochs, batch_size=2) # (49.1, 21.0, 74.2), (x, y) = (-34.6, 128.0)
        return model

    def sample_from_output(self, params, num_samples=1):
        print(params)
        return [params]