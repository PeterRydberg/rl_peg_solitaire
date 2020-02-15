import random


class Actor:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor,
        e_greediness,
        episodes
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.e_greediness = e_greediness
        self.e_greediness_decrease = e_greediness / episodes

        self.eligibilities = {}
        self.policy = {}

    # Adds new state and actions policy
    def add_sap_policy(self, state, action):
        if(state not in self.policy.keys()):
            self.policy[state] = {}

        self.policy[state][action] = 0

    # Updates state and actions policy
    def update_sap_policy(self, state, action, temporal_diff):
        self.policy[state][action] += \
            self.learning_rate * \
            temporal_diff * \
            self.eligibilities[state][action]

    # Gets the new move for current state
    def get_move(self, current_state):
        # Uses e-greediness to determine best or random move
        if(random.uniform(0, 1) < 1 - self.e_greediness):
            # Returns the best policy move
            return max(
                self.policy[current_state],
                key=(lambda key: self.policy[current_state][key])
            )
        else:
            # Returns a random move
            return random.choice(list(self.policy[current_state].keys()))

    # Updates eligibilities
    def update_eligibilities(self, state, action, decay=False):
        # If the state does is not initialized
        if(state not in self.eligibilities.keys()):
            self.eligibilities[state] = {}

        # Check whether to decay or set to 1
        if(not decay):
            self.eligibilities[state][action] = 1
        else:
            self.eligibilities[state][action] = \
                self.discount_factor * \
                self.eligibility_decay * \
                self.eligibilities[state][action]

    # Reset all eligibilities
    def reset_eligibilities(self):
        for state in self.eligibilities:
            for action in state:
                self.eligibilities[state][action] = 0

    # Decrease greediness episodically, eventually zero
    def increase_greediness(self, episodes):
        self.e_greediness -= self.e_greediness_decrease

    def set_greedy(self):
        self.e_greediness = 0
