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

    # Update SAP and eligibilities for each action
    def actions_update(self, actions_taken, temporal_diff):
        # Update eligibility for the board state and action used
        prev_state, prev_action = actions_taken[-1]
        self.update_eligibilities(
            state=prev_state,
            action=prev_action,
            decay=False
        )

        for state, action in actions_taken:
            # Update actor values and actor eligibility
            self.update_sap_policy(state, action, temporal_diff)
            self.update_eligibilities(state, action, True)

    # Gets the new move for current state
    def get_move(self, current_state, legal_moves=None, training=False):
        # If the choice is not meant to alter the model, but the state
        # does not exist in its policy after training: Return random legal move
        if(training is False and current_state not in self.policy.keys()):
            return random.choice(legal_moves)

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

    # Decrease greediness episodically, eventually zero
    def increase_greediness(self, episodes):
        self.e_greediness -= self.e_greediness_decrease

    def set_greedy(self):
        self.e_greediness = 0

    def handle_board_state(self, board_state, legal_moves):
        # Add the board state and actions if not in policy
        if(board_state not in self.policy.keys()):
            for action in legal_moves:
                self.add_sap_policy(board_state, action)
