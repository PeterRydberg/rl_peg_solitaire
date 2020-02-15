import random


class CriticTable:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor

        self.eligibilities = {}
        self.values = {}

    # Adds new state value
    def add_state_value(self, current_state):
        self.values[current_state] = random.uniform(0, 0.1)

    # Updates state value
    def update_state_value(self, state, temporal_diff):
        self.values[state] += \
            self.learning_rate * \
            temporal_diff * \
            self.eligibilities[state]

    # Updates eligibilities
    def update_eligibilities(self, state, decay=False):
        # Check whether to decay or set to 1
        if(not decay):
            self.eligibilities[state] = 1
        else:
            self.eligibilities[state] = \
                self.discount_factor * \
                self.eligibility_decay * \
                self.eligibilities[state]

    # Reset all eligibilities
    def reset_eligibilities(self):
        for i in self.eligibilities:
            self.eligibilities[i] = 0

    # Calculates temporal difference for the new state
    def calc_temp_diff(self, reward, current_state, previous_state):
        # Add the board state if not in values
        if(current_state not in self.values.keys()):
            self.add_state_value(current_state)

        return \
            reward + \
            (self.discount_factor * self.values[current_state]) - \
            self.values[previous_state]

    def handle_board_state(self, board_state):
        # Add the board state if not in values
        if(board_state not in self.values.keys()):
            self.add_state_value(board_state)
