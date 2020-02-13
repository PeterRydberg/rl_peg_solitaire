import random


class Actor:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor,
        e_greediness
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.e_greediness = e_greediness

        self.eligibilities = {}
        self.policy = {}

    def initialize_actor(self):
        pass

    # Adds new state and actions policy
    def update_policy(self, current_state, legal_moves):
        self.policy[current_state] = {}

        for legal_move in legal_moves:
            self.policy[current_state][legal_move] = 0

    # Updates eligibilities
    def update_eligibilities(self, current_state, update_state):
        if(current_state == update_state):
            self.eligibilities[update_state] = 1
        else:
            self.eligibilities[update_state] = self.discount_factor * \
                self.eligibility_decay * self.eligibilities[update_state]

    # Reset all elegibilities
    def reset_elegibilities(self):
        for i in self.eligibilities:
            self.eligibilities[i] = 1

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
