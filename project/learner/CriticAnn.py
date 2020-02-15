class CriticAnn:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor,
        nn_layers
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.nn_layers = nn_layers

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
