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
        pass  # ANN does not need a dictionary update

    # Updates state value
    def update_state_value(self, state, temporal_diff):
        for i, layer in enumerate(self.model.parameters()):
            for j, node_weights in enumerate(layer):
                node_weights = \
                    node_weights + \
                    self.learning_rate * \
                    temporal_diff * \
                    self.eligibilities[state][i][j]
            self.optimizer.step()

    # Updates eligibilities
    def update_eligibilities(self, state, decay=False):
        if(not decay):
            # If state is not in the eligibility trace
            if(state not in self.eligibilities.keys()):
                self.eligibilities[state] = {}

            for i, layer in enumerate(self.model.parameters()):
                # If the layer is not in the state-layer eligibility trace
                if(i not in self.eligibilities[state].keys()):
                    self.eligibilities[state][i] = {}

                for j in range(len(layer)):
                    # Set the node weight eligibility to 1
                    self.eligibilities[state][i][j] = torch.ones(
                        layer[j].size()
                    )
        else:
            for i, layer in enumerate(self.model.parameters()):
                for j in range(len(layer)):
                    self.eligibilities[state][i][j] = \
                        self.eligibilities[state][i][j] + \
                        layer.grad[j]

    # Reset all eligibilities
    def reset_eligibilities(self):
        # For every weight in a state eligibility dictionary, set to zero
        for state in self.eligibilities:
            for layer in self.eligibilities[state]:
                for node in self.eligibilities[state][layer]:
                    self.eligibilities[state][layer][node] = torch.zeros(
                        self.eligibilities[state][layer][node].size()
                    )

    # Update SAP and eligibilities for each action
    def actions_update(self, actions, temporal_diff):
        # Update eligibility and weights for the board state used
        prev_state, _ = actions[-1]

        self.model.zero_grad()
        loss = self.get_loss_from_temp_diff(temporal_diff)
        loss.backward()

        self.update_eligibilities(
            state=prev_state,
            decay=False
        )

        with torch.no_grad():
            for state, _ in actions:
                # Update critic values and critic eligibility
                self.update_eligibilities(state, True)
                self.update_state_value(state, temporal_diff)

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
