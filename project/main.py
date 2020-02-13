from learner.ReinforcementLearner import ReinforcementLearner
from learner_settings import tri_5_table, diam_4_table


def main():
    settings = diam_4_table

    try:
        rl_learner = ReinforcementLearner(
            episodes=settings["episodes"],
            game_settings=settings["game_settings"],
            critic_settings=settings["critic_settings"],
            actor_settings=settings["actor_settings"]
        )
        rl_learner.train_model()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
