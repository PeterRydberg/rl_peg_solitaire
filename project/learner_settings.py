# See README.md for explanation of all settings


tri_5_table = {
    "episodes": 1000,

    "game_settings": {
        "board_type": "triangle",
        "board_size": 5,
        "initial_empty": {},
        "live_update_frequency": 0.2,
        "display_game": (1, 50, 500)
    },

    "critic_settings": {
        "c_type": "table",
        "c_learning_rate": 0.1,
        "c_eligibility_decay": 0.99,
        "c_discount_factor": 0.99,
        "c_nn_layers": [1, 2, 3]
    },

    "actor_settings": {
        "a_learning_rate": 0.1,
        "a_eligibility_decay": 0.99,
        "a_discount_factor": 0.99,
        "a_e_greediness": 0.5
    }
}

diam_4_table = {
    "episodes": 1000,

    "game_settings": {
        "board_type": "diamond",
        "board_size": 4,
        "initial_empty": {},
        "live_update_frequency": 0.2,
        "display_game": ()  # (1, 50, 500)
    },

    "critic_settings": {
        "c_type": "table",
        "c_learning_rate": 0.1,
        "c_eligibility_decay": 0.99,
        "c_discount_factor": 0.99,
        "c_nn_layers": [1, 2, 3]
    },

    "actor_settings": {
        "a_learning_rate": 0.1,
        "a_eligibility_decay": 0.99,
        "a_discount_factor": 0.99,
        "a_e_greediness": 0.5
    }
}

tri_5_ann = {
    "episodes": 500,

    "game_settings": {
        "board_type": "triangle",
        "board_size": 5,
        "initial_empty": {},
        "live_update_frequency": 0.2,
        "display_game": ()  # (1, 50, 500)
    },

    "critic_settings": {
        "c_type": "ann",
        "c_learning_rate": 0.001,
        "c_eligibility_decay": 0.99,
        "c_discount_factor": 0.99,
        "c_nn_layers": [15, 5]
    },

    "actor_settings": {
        "a_learning_rate": 0.1,
        "a_eligibility_decay": 0.99,
        "a_discount_factor": 0.99,
        "a_e_greediness": 0.5
    }
}

diam_4_ann = {
    "episodes": 500,

    "game_settings": {
        "board_type": "diamond",
        "board_size": 4,
        "initial_empty": {},
        "live_update_frequency": 0.2,
        "display_game": ()  # (1, 50, 500)
    },

    "critic_settings": {
        "c_type": "ann",
        "c_learning_rate": 0.001,
        "c_eligibility_decay": 0.99,
        "c_discount_factor": 0.99,
        "c_nn_layers": [15, 5]
    },

    "actor_settings": {
        "a_learning_rate": 0.1,
        "a_eligibility_decay": 0.99,
        "a_discount_factor": 0.99,
        "a_e_greediness": 0.5
    }
}
