class Actor:
    def __init__(self, learning_rate, eligibility_decay, discount_factor, e_greediness):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.e_greediness = e_greediness

        self.eligibilities = {}
