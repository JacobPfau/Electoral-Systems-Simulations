from abc import ABC, abstractmethod
import numpy as np

class Voter(ABC):
    def __init__(self, utilities=dict(), beliefs=None):
        '''
        Params
        policy: dict str to object, defines the voter's policy under electoral systems
        utility: dict str to float, defines the voter's utility gained from electoral outcomes
        beliefs: ...
        '''
        self.utilities = utilities
        self.beliefs = beliefs
        self.vote = dict()

    @abstractmethod
    def policy(self, electoral_system):
        pass

class Laziest_Voter(Voter):
    def policy(self, electoral_system):
        if electoral_system.name=='ApprovalVote' or electoral_system.name=='PluralityVote': # Should separate these for clarity/consistency
            favorite = [*list(self.utilities.items())[0]]
            for candidate, utility in self.utilities.items():
                if utility>favorite[1]: favorite = [candidate, utility]
            self.vote[favorite[0]] = 1
            if electoral_system.name=='ApprovalVote': # Fill in the other candidates with 0s
                for candidate in self.utilities.keys():
                    if candidate!= favorite[0]: self.vote[candidate] = 0
            return self.vote
        else:
            raise NotImplementedError

class Lazy_Voter(Voter):
    def policy(self, electoral_system):
        if electoral_system.name=='ApprovalVote':
            utility_list = list(self.utilities.items())
            utility_list = sorted(utility_list, key=lambda x:x[1], reverse=True)
            votes = {candidate:0 for candidate in self.utilities.keys()}
            votes[utility_list[0][0]]=1
            votes[utility_list[1][0]]=1
            self.vote = votes
            return self.vote
        else:
            raise NotImplementedError

class Honest_Voter(Voter):
    def policy(self, electoral_system):
        if electoral_system.name=='ApprovalVote':
            median_utility = np.median(list(self.utilities.values()))
            votes = {candidate:0 for candidate in self.utilities.keys()}
            for candidate, utility in self.utilities.items():
                if utility>=median_utility: votes[candidate]=1
            self.vote = votes
            return self.vote
        elif electoral_system.name=='PluralityVote':
            favorite = [*list(self.utilities.items())[0]]
            for candidate, utility in self.utilities.items():
                if utility>favorite[1]: favorite = [candidate, utility]
            self.vote[favorite[0]] = 1
            return self.vote
        else:
            raise NotImplementedError