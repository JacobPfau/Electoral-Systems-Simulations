import numpy as np
import copy

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

        self.vote = dict() # List for IRV
    
    def generate_utilities(self, candidate_ideologies):
        raise NotImplementedError
    
    def compute_vote(self, electoral_system):
        self.vote = dict()
        if electoral_system=='ApprovalVote': self.approval_policy()
        elif electoral_system=='PluralityVote': self.plurality_policy()
        elif electoral_system=='InstantRunoffVote': self.irv_policy()

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
        favorite_candidate = max(self.utilities.items(), key=lambda x:x[1])[0]
        self.vote[favorite_candidate] = 1
        return self.vote
    
    def irv_policy(self,):
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        return self.vote

class Laziest_Voter(Honest_Voter):
    def approval_policy(self,):
        '''
        Only vote for one candidate
        '''
        favorite_candidate = max(self.utilities.items(), key=lambda x:x[1])[0]
        for candidate in self.utilities.keys():
            if candidate!= favorite_candidate: self.vote[candidate] = 0
        return self.vote
    def plurality_policy(self):
        return super().plurality_policy()
    def irv_policy(self):
        '''
        Swap one of the non-favorite candidates with adjacent candidate
        '''
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        swap = np.random.choice(range(1,len(self.vote)-1))
        to_swap = copy.copy(self.vote[swap])
        self.vote[swap] = self.vote[swap-1]
        self.vote[swap-1] = to_swap
        return self.vote


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