import numpy as np
import gym
from sarsa_lambda import SarsaLambda
# from tamer import TAMER
from tamer_nai import TAMER
from model import StateActionFeatureVectorWithTile
import argparse
import matplotlib.pyplot as plt

def plot_returns(G):
    plt.plot(G)
    plt.xlabel('Episode')
    plt.ylabel('Returns')
    plt.show()

def run_sarsa_lamda(args):
    env = gym.make(args.env)
    gamma = 1.

    TAMER(env, 0.9, args.verbose, 10)
    quit()

    X = StateActionFeatureVectorWithTile(
        env.observation_space.low,
        env.observation_space.high,
        env.action_space.n,
        num_tilings=10,
        tile_width=np.array([.45,.035])
    )

    if args.load_path == None:
        w = SarsaLambda(env, gamma, 0.8, 0.01, X, args.iter, args.verbose)
        np.save(args.save_path, w)
    else:
        w = np.load(args.load_path)

    def greedy_policy(s,done):
        Q = [np.dot(w, X(s,done,a)) for a in range(env.action_space.n)]
        return np.argmax(Q)

    def _eval(render=False):
        s, done = env.reset(), False
        if render: env.render()

        G = 0.
        while not done:
            a = greedy_policy(s,done)
            s,r,done,_ = env.step(a)
            if render: env.render()

            G += r
        return G

    # MountainCar-v0 defines "solving" as getting average reward of -110.0 over 100 consecutive trials.
    print("Evaluating")
    Gs = [_eval() for _ in  range(100)]
    print("Average reward over 100 trials: ", np.mean(Gs))
    _eval(True)

    plot_returns(Gs)


if __name__ == "__main__":
    """
    Example usage 
    python3 run.py --verbose --iter 10 --load_path weights.npy
    """

    parser = argparse.ArgumentParser(description='RL-Project')
    parser.add_argument('--env', type=str, default='MountainCar-v0')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--save_path', type=str, default='weights.npy')
    parser.add_argument('--load_path', type=str, default=None)
    parser.add_argument('--iter', type=int, default=2000, help="How many iterations to run the algorithm for")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--lambda', type=float, default=0.8, help="lambda")

    args = parser.parse_args()
    run_sarsa_lamda(args)
