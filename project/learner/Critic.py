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

    def update_eligibilities(self, current_state, update_state):
        if(current_state == update_state):
            self.eligibilities[update_state] = 1
        else:
            self.eligibilities[update_state] = self.discount_factor * \
                self.eligibility_decay * self.eligibilities[update_state]

    def reset_elegibilities(self):
        for i in self.eligibilities:
            self.eligibilities[i] = 1
