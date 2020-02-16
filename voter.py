class Voter():
    def __init__(self, policy, utilities=dict(), beliefs=None):
        '''
        Params
        policy: dict str to object, defines the voter's policy under electoral systems
        utility: dict str to float, defines the voter's utility gained from electoral outcomes
        beliefs: ...
        '''
        self.policy = policy
        self.utilities = utilities
        self.beliefs = beliefs
        self.vote = dict()

    def get_vote(self, candidates, electoral_system):
        self.vote = self.policy(self, candidates, electoral_system)