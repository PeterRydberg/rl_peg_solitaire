from learner.ReinforcementLearner import ReinforcementLearner
from learner_settings import tri_5_table, diam_4_table, tri_5_ann, diam_4_ann


def main():
    settings = tri_5_ann

    try:
        # Creates and trains model
        rl_learner = ReinforcementLearner(
            episodes=settings["episodes"],
            game_settings=settings["game_settings"],
            critic_settings=settings["critic_settings"],
            actor_settings=settings["actor_settings"]
        )
        performance = rl_learner.train_model()

        # Display performance graph
        rl_learner.display_performance_graph(performance)

        # Makes a test run
        rl_learner.run_game()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
