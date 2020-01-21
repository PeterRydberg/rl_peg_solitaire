class Critic:
    def __init__(self, critic_type, learning_rate, discount_factor, nn_layers=(1,2,3)):
        self.critic_type = critic_type
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.nn_layers = nn_layers

        self.eligibilities = {}
        self.values = {}
