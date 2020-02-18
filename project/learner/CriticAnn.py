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

        self.eligibilities = {}

        self.model = self.create_pytorch_model(
            nn_layers,
            input_shape,
            learning_rate
        )
        # self.optimizer = torch.optim.Adam(
        #    self.model.parameters(),
        #    self.learning_rate
        # )

        self.optimizer = torch.optim.SGD(
            self.model.parameters(),
            self.learning_rate,
            0.9
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
        model.add_module('sigmoid_out', torch.nn.Sigmoid())

        return model

    # Adds new state value
    def add_state_value(self, current_state):
        pass  # ANN does not need a dictionary update

    # Updates state value
    def update_state_value(self, temporal_diff):
        for i, layer in enumerate(self.model.parameters()):
            for j, node_weights in enumerate(layer):
                node_weights = \
                    node_weights + \
                    self.learning_rate * \
                    temporal_diff * \
                    self.eligibilities[i][j]
            self.optimizer.step()

    # Updates eligibilities
    def update_eligibilities(self, decay=False):
        if(not decay):
            for i, layer in enumerate(self.model.parameters()):
                # If the layer is not in the state-layer eligibility trace
                if(i not in self.eligibilities.keys()):
                    self.eligibilities[i] = {}

                for j in range(len(layer)):
                    # If the layer is not in the state-layer eligibility trace
                    if(j not in self.eligibilities[i].keys()):
                        self.eligibilities[i][j] = torch.zeros(
                            layer[j].size()
                        )

                    self.eligibilities[i][j] = \
                        self.eligibilities[i][j] + \
                        layer.grad[j]
        else:
            for i, layer in enumerate(self.model.parameters()):
                for j in range(len(layer)):
                    self.eligibilities[i][j] = \
                        self.discount_factor * \
                        self.eligibility_decay * \
                        self.eligibilities[i][j]

    # Reset all eligibilities
    def reset_eligibilities(self):
        # For every weight in the net eligibility dictionary, set to zero
        for layer in self.eligibilities:
            for node in self.eligibilities[layer]:
                self.eligibilities[layer][node] = torch.zeros(
                    self.eligibilities[layer][node].size()
                )

    # Update SAP and eligibilities for each action
    def actions_update(self, actions_taken, temporal_diff):
        self.model.zero_grad()
        loss = self.get_loss_from_temp_diff(temporal_diff)
        loss.backward()
        # print(temporal_diff)
        # print(loss)
        for layer in self.model.parameters():
            print("layer", layer)
            print("grad", layer.grad)

        # Update elegibility of the neural net
        self.update_eligibilities(
            decay=False
        )

        with torch.no_grad():
            for _ in actions_taken:
                # Update critic values and critic eligibility
                self.update_state_value(temporal_diff)
                self.update_eligibilities(True)  # Decay all elegibilities

    # Calculates temporal difference for the new state
    def calc_temp_diff(self, reward, current_state, previous_state):
        return \
            reward + \
            (self.discount_factor * self.get_val_from_state(current_state)) - \
            self.get_val_from_state(previous_state)

    # Mean squared error from initial TD error
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
