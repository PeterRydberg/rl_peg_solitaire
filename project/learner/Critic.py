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

    def update_eligibilities(self, state, legal_moves):
        # TODO: Calculate values. Add state to val if not exist
        pass
