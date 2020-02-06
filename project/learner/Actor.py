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

    def update_policy(self, current_state, legal_moves):
        pass

    def update_eligibilities(self, current_state, update_state):
        if(current_state == update_state):
            self.eligibilities[update_state] = 1
        else:
            self.eligibilities[update_state] = self.discount_factor * \
                self.eligibility_decay * self.eligibilities[update_state]

    def reset_elegibilities(self):
        for i in self.eligibilities:
            self.eligibilities[i] = 1

    def make_move(self):
        if(random.uniform(0, 1) < 1 - self.e_greediness):
            return max(self.policy, key=(lambda key: self.policy[key]))
        else:
            return random.choice(list(self.policy.keys()))
