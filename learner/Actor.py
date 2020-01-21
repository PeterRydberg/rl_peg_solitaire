class Actor:
    def __init__(self, learning_rate, discount_factor, e_probability):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.e_probability = e_probability

        self.eligibilities = {}
