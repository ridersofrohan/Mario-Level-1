# Keeps track of the previous action that it took to get to a state

import helpers

import gym
import numpy as np
import random
import copy
import math
from collections import defaultdict

EXPLORATION_PROB = 0.15
NUM_ITERS = 10000

def simple_rl(previousWeights={}):
    env = gym.make('SuperMarioBros-1-1-v0')

    eta = 1.0 / math.sqrt(NUM_ITERS)
    discount = .95

    if previousWeights == {}:
        weights = defaultdict(float)
    else:
        weights = previousWeights

    actions = {
        #0: [0, 0, 0, 0, 0, 0],  # Nothing
        1: [1, 0, 0, 0, 0, 0],  # Up
        2: [0, 0, 1, 0, 0, 0],  # Down
        3: [0, 1, 0, 0, 0, 0],  # Left
        #4: [0, 1, 0, 0, 1, 0],  # Left + A
        #5: [0, 1, 0, 0, 0, 1],  # Left + B
        #6: [0, 1, 0, 0, 1, 1],  # Left + A + B
        7: [0, 0, 0, 1, 0, 0],  # Right
        8: [0, 0, 0, 1, 1, 0],  # Right + A
        9: [0, 0, 0, 1, 0, 1],  # Right + B
        10: [0, 0, 0, 1, 1, 1],  # Right + A + B
        11: [0, 0, 0, 0, 1, 0],  # A
        12: [0, 0, 0, 0, 0, 1],  # B
        13: [0, 0, 0, 0, 1, 1],  # A + B
        14: [1, 0, 0, 0, 1, 0],  # Up + A
    }

    def random_action():
        return random.sample(actions.keys(), 1)[0]

    def featureExtractor(state, action):
        features = []
        featureKey = (state, action)
        features.append((featureKey,1))
        for i,button in enumerate(actions[action]):
            buttonPressed = [0] * len(actions[action])
            buttonPressed[i] = button
            features.append(((state, " ".join(str(x) for x in buttonPressed)),1))
        marioIndex = state.find('3')
        if marioIndex == -1: return features
        if state[marioIndex+2] == '1' or state[marioIndex-2] == '1':
            features.append(('nextToWall', 1))
        else:
            features.append(('nextToWall', 0))
        if state[marioIndex+2] == '2' or state[marioIndex-2] == '2':
            features.append(('nextToGoomba', 1))
        else:
            features.append(('nextToGoomba', 0))
        return features

    def getQ(state, action):
        score = 0
        for f, v in featureExtractor(state, action):
            score += weights[f] * v
        return score

    def getAction(state):
        if random.random() < EXPLORATION_PROB:
            return random_action()
        else:
            return max((getQ(state, action), action) for action in actions.keys())[1]

    def generate_reward(oldInfo, newInfo, oldAction, newAction, farthestTraveled):
        reward = 0
        if oldInfo == {} or not oldAction:
            return reward
        timeDelta = 1/(newInfo['time']+1)
        distanceDelta = newInfo['distance'] - oldInfo['distance']
        if distanceDelta > 0:
            if newInfo['distance'] > farthestTraveled:
                reward += distanceDelta
            else: reward += distanceDelta*0.1 - timeDelta
        else: reward += distanceDelta - timeDelta
        scoreDelta = newInfo['score'] - oldInfo['score']
        reward += scoreDelta
        if oldAction == newAction:
            reward *= 2
        if action == 0: reward -= timeDelta
        return reward

    def incorporateFeedback(state, action, reward, newState):
        vOpt = max([getQ(newState, aPrime) for aPrime in actions.keys()]) if len(newState) > 0 else 0
        qOpt = getQ(state,action)
        scale = eta * (qOpt - (reward + (discount*vOpt)))
        for f,v in featureExtractor(state, action):
            weights[f] -= scale*v

    for episode in range(1, NUM_ITERS):
        env.lock.acquire()
        currentState = str(env.reset())
        env.lock.release()

        succ, oldAction, done, gameOver = None, None, False, False
        totalReward, reward, previousAction, bestDistance = 0, 0, 0, 0
        oldInfo, info = {}, {}
        farthestTraveled = 0

        for i in range(1, 100000):
            env.render()

            if oldInfo:
                farthestTraveled = max(farthestTraveled, oldInfo['distance'])
            action = getAction(currentState)
            '''
            while action == None:
                action = getAction(currentState)
                print("WE HAVE A NONE ACTION!!!!")
                print(qTable[str(s)][previousAction])
            '''
            succ, ogReward, done, info = env.step(actions[action])
            reward = generate_reward(oldInfo, info, oldAction, action, farthestTraveled)
            succState = str(succ)
            print("OgReward: {}".format(ogReward))
            print("OurReward: {}".format(reward))
            print(currentState)
            print(i, actions[action], reward)

            incorporateFeedback(currentState, action, reward, succState)

            if info['life'] == 0:
                reward = -50
                gameOver = True
            if done:
                reward = 2000

            totalReward += reward

            if info['distance'] > bestDistance:
                bestDistance = info['distance']

            if gameOver or done:
                break

            currentState = succState
            oldInfo = copy.deepcopy(info)
            oldAction = action
            previousAction = action

        print("Episode: {} \t Reward: {} \t Distance: {}".format(episode, totalReward, bestDistance))

        with open('rewards_funcApprox.txt', 'a') as f:
            f.write(str([episode, totalReward, bestDistance]))
            f.write("\n")
        f.close()

        if episode % 5 == 0:
            helpers.write_to_file("weights_funcApprox.pickle", weights, True)

        if episode % 15 == 0:
            with open('weights_funcApprox.txt', 'a') as f:
                f.write(str([episode, weights]))
                f.write("\n")
            f.close()

        env.lock.acquire()
        env.close()
        env.lock.release()
        helpers.killFCEUX()
    os._exit(0)

if __name__ == '__main__':
  simple_rl()
  #simple_rl(helpers.read_in_data('weights.pickle'))


