import random


class Critic:
    def __init__(
        self,
        critic_type,
        learning_rate,
        eligibility_decay,
        discount_factor,
        nn_layers
    ):
        self.critic_type = critic_type
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.nn_layers = nn_layers

        self.eligibilities = {}
        self.values = {}

    def initialize_critic(self):
        pass

    # Adds new state value
    def add_state_value(self, current_state):
        self.values[current_state] = random.uniform(0, 0.1)

    def calc_temp_diff(self, reward, current_state, previous_state):
        # Add the board state if not in values
        if(current_state not in self.values.keys()):
            self.add_state_value(current_state)

        return \
            reward + \
            (self.discount_factor * self.values[current_state]) - \
            self.values[previous_state]

    def update_eligibilities(self, current_state, update_state):
        if(current_state == update_state):
            self.eligibilities[update_state] = 1
        else:
            self.eligibilities[update_state] = self.discount_factor * \
                self.eligibility_decay * self.eligibilities[update_state]

    def reset_elegibilities(self):
        for i in self.eligibilities:
            self.eligibilities[i] = 1
