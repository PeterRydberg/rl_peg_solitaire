class CriticAnn:
    def __init__(
        self,
        learning_rate,
        eligibility_decay,
        discount_factor,
        nn_layers
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = eligibility_decay
        self.discount_factor = discount_factor
        self.nn_layers = nn_layers
