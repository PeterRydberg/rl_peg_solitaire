import tensorflow as tf
from .split_dg import SplitDG


class CriticAnn:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor,
        nn_layers,
        input_shape
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor

        self.model = self.create_model(nn_layers, input_shape, learning_rate)
        self.gradients = SplitDG(self.model)

    # Adds new state value
    def add_state_value(self, current_state):
        pass

    # Updates state value
    def update_state_value(self, state, temporal_diff):
        pass

    # Updates eligibilities
    def update_eligibilities(self, state, decay=False):
        pass

    # Reset all eligibilities
    def reset_eligibilities(self):
        pass

    # Calculates temporal difference for the new state
    def calc_temp_diff(self, reward, current_state, previous_state):
        pass

    def handle_board_state(self, board_state):
        pass  # ANN does not need a dictionary update

    def create_model(self, nn_layers, input_shape, learning_rate):
        model = tf.keras.Sequential()

        # Layer with initial input shape
        model.add(
            tf.keras.layers.Dense(
                nn_layers[0],
                activation='relu',
                input_shape=(input_shape,)
            )
        )

        # All but the first hidden layer
        for layer in nn_layers[1:]:
            model.add(tf.keras.layers.Dense(layer, activation='relu'))

        # One output value
        model.add(tf.keras.layers.Dense(1))

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate),
            loss='mse',
            metrics=['accuracy', 'mae']
        )
        return model
