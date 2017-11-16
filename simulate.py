import sys
import cProfile
import collections, random
import pygame as pg
import time

from data.main import MarioLevel
from agents import MarioMDP, SimpleAgent
from util import RLAlgorithm


def simulate(mdp, rl, numTrials=10, maxIterations=10000, verbose=False, sort=False):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    for trial in range(numTrials):
        game = MarioLevel(agent=agent)
        state = mdp.startState()
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        for _ in range(maxIterations):
            action = rl.getAction(state)
            transitions = mdp.succAndProbReward(state, action)
            if sort: transitions = sorted(transitions)
            if len(transitions) == 0:
                rl.incorporateFeedback(state, action, 0, None)
                break

            # Choose a random transition
            i = sample([prob for newState, prob, reward in transitions])
            newState, prob, reward = transitions[i]
            sequence.append(action)
            sequence.append(reward)
            sequence.append(newState)

            rl.incorporateFeedback(state, action, reward, newState)
            totalReward += totalDiscount * reward
            totalDiscount *= mdp.discount()
            state = newState
        if verbose:
            print "Trial %d (totalReward = %s): %s" % (trial, totalReward, sequence)
        totalRewards.append(totalReward)
    return totalRewards


# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]


def testSimulate():
    agent = SimpleAgent()
    game = MarioLevel(agent=agent)
    game.progress()
    game.progress()
    game.progress()

    for i in range(1000):
        game.progress(action=agent.getAction())


if __name__=='__main__':
    # mdp = MarioMDP()
    # ql = QLearningAlgorithm(mdp.actions, mdp.discount(), identityFeatureExtractor)
    # simulation = util.simulate(mdp, ql, 30000)
    testSimulate()
