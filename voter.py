import numpy as np

class Voter():
    def __init__(self, ideology=None, utilities=None, beliefs=None):
        '''
        Params
        ideology: np array, defines the voters location in n-dimensional ideology vector space
        policy: dict str to object, defines the voter's policy under electoral systems
        utility: None or dict str to float, defines the voter's utility gained from electoral outcomes
        beliefs: not implemented, for strategic voting purposes
        '''
        self.utilities = utilities
        self.beliefs = beliefs
        self.ideology = ideology

        self.vote = dict()
    
    def generate_utilities(self, candidate_ideologies):
        raise NotImplementedError

    def approval_policy(self,):
        raise NotImplementedError
    def plurality_policy(self,):
        raise NotImplementedError
    def irv_policy(self,):
        raise NotImplementedError
    def quadratic_policy(self,):
        raise NotImplementedError

class Honest_Voter(Voter):
    def approval_policy(self,):
        # Votes for all candidates with >= voters median utility
        median_utility = np.median(list(self.utilities.values()))
        votes = {candidate:0 for candidate in self.utilities.keys()}
        for candidate, utility in self.utilities.items():
            if utility>=median_utility: votes[candidate]=1
        self.vote = votes
        return self.vote

    def plurality_policy(self):
        favorite = [*list(self.utilities.items())[0]]
        for candidate, utility in self.utilities.items():
            if utility>favorite[1]: favorite = [candidate, utility]
        self.vote[favorite[0]] = 1
        return self.vote


class Laziest_Voter(Honest_Voter):
    def approval_policy(self,):
        # Only vote for one candidate
        favorite = [*list(self.utilities.items())[0]]
        for candidate, utility in self.utilities.items():
            if utility>favorite[1]: favorite = [candidate, utility]
        self.vote[favorite[0]] = 1
        for candidate in self.utilities.keys():
            if candidate!= favorite[0]: self.vote[candidate] = 0
        return self.vote
    def plurality_policy(self):
        # Behave honestly here
        return super().plurality_policy()


class Lazy_Voter(Honest_Voter):
    def approval_policy(self,):
        # Vote for top two candidates regardless of num candidates
        utility_list = list(self.utilities.items())
        utility_list = sorted(utility_list, key=lambda x:x[1], reverse=True)
        votes = {candidate:0 for candidate in self.utilities.keys()}
        votes[utility_list[0][0]]=1
        votes[utility_list[1][0]]=1
        self.vote = votes
        return self.vote
    def plurality_policy(self):
        # Behave honestly here
        return super().plurality_policy()