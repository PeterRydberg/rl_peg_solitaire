# import tensorflow as tf
# import SplitDG

import torch


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

        # self.model = self.create_keras_model(nn_layers, input_shape,
        # learning_rate)
        # self.gradients = SplitDG(self.model)

        self.model = self.create_pytorch_model(
            nn_layers,
            input_shape,
            learning_rate
        )
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            self.learning_rate
        )

    def create_pytorch_model(self, nn_layers, input_shape, learning_rate):
        model = torch.nn.Sequential()
        layers = nn_layers.copy()
        layers.insert(0, input_shape)  # Input layer
        layers.append(1)  # Output layer

        # Layer with initial input shape
        model.add_module('input', torch.nn.Linear(input_shape, nn_layers[0]))
        model.add_module('relu_in', torch.nn.ReLU())

        # All but the input and output layers (hidden layers)
        for i, layer in enumerate(nn_layers):
            model.add_module(
                f'layer{i+1}', torch.nn.Linear(layer, layers[i+2])
            )
            model.add_module(f'relu{i+1}', torch.nn.ReLU())

        # One output value
        model.add_module('output', torch.nn.Linear(1, 1))
        model.add_module('relu_out', torch.nn.ReLU())

        return model

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
        return \
            reward + \
            (self.discount_factor * self.get_val_from_state(current_state)) - \
            self.get_val_from_state(previous_state)

    def get_loss_from_temp_diff(self, temp_diff):
        return torch.mean(temp_diff**2)

    # Gets a new model prediction from state
    def get_val_from_state(self, state):
        tensor = torch.Tensor(self.state_to_tensor(state))
        return self.model(tensor)

    # Converts state to tensor representation
    def state_to_tensor(self, state):
        bitlist = list(state)
        return torch.tensor(list(map(float, bitlist)))

    def handle_board_state(self, board_state):
        pass  # ANN does not need a dictionary update


'''
    def create_keras_model(self, nn_layers, input_shape, learning_rate):
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
'''
