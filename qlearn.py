import util, math, random
from collections import defaultdict
from util import ValueIteration

class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        vOpt = max([self.getQ(newState, aPrime) for aPrime in self.actions(newState)]) if newState else 0
        qOpt = self.getQ(state,action)
        for f,v in self.featureExtractor(state, action):
            self.weights[f] = (1-self.getStepSize()) * qOpt + self.getStepSize()*(reward + (self.discount*vOpt))
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    valueIteration = ValueIteration() 
    valueIteration.solve(mdp)
    viPolicy = valueIteration.pi
    ql = QLearningAlgorithm(mdp.actions, mdp.discount(), featureExtractor)
    simulation = util.simulate(mdp, ql, 30000)
    ql.explorationProb = 0
    numDiff = 0.0
    differences = defaultdict(float)
    numSame = 0.0
    for key,action in viPolicy.items():
        qlAction = ql.getAction(key)
        if qlAction != action:
            differences[(action, qlAction)] += 1
            numDiff += 1
        else:
            numSame += 1
    print numDiff 
    print numSame
    print differences
    # END_YOUR_CODE


